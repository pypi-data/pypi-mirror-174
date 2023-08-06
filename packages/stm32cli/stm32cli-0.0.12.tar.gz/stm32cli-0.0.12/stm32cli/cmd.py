import colorama
from .uart import UART
from .bsp import delay, millis


class CmdPacket:
  cmd = 0
  dir = 0
  error = 0
  length = 0
  check_sum = 0
  check_sum_recv = 0
  buffer = []
  data= 0

class CMD:
  
  CMD_OK  =                 0
  
  CMD_DIR_M_TO_S  =         0
  CMD_DIR_S_TO_M  =         1
  
  CMD_STX =                 0x02
  CMD_EXT =                 0x03

  CMD_STATE_WAIT_STX=       0
  CMD_STATE_WAIT_CMD=       1
  CMD_STATE_WAIT_DIR=       2
  CMD_STATE_WAIT_ERROR=     3
  CMD_STATE_WAIT_LENGTH_L=  4
  CMD_STATE_WAIT_LENGTH_H=  5
  CMD_STATE_WAIT_DATA=      6
  CMD_STATE_WAIT_CHECKSUM=  7
  CMD_STATE_WAIT_ETX=       8

  CMD_MAX_DATA_LENGTH=      256
  
  is_init = False
  state = CMD_STATE_WAIT_STX
  pre_time = 0
  index = 0
  error = 0
  rx_packet = CmdPacket()
  tx_packet = CmdPacket()
  
  def __init__(self, ch, baud):
    self.uart = UART(ch, baud)
    
  def init(self):
    self.is_init = True
    self.state = self.CMD_STATE_WAIT_STX

  def open(self):
    self.pre_time = millis()
    return self.uart.open()
  
  def close(self):
    return self.uart.close()
  
  def cmdReceivePacket(self):
    ret = False
    rx_data = 0
    if(self.uart.available()):
      rx_data = self.uart.read()
    else:
      return False
    if(millis() - self.pre_time >= 100):
      self.state = self.CMD_STATE_WAIT_STX
      return False
    
    self.pre_time = millis()
    
    rx_data = int.from_bytes(rx_data, "little")
    match self.state:
      case  self.CMD_STATE_WAIT_STX:
        if(rx_data == self.CMD_STX):
          self.state = self.CMD_STATE_WAIT_CMD
          self.rx_packet.check_sum = 0
      
      case self.CMD_STATE_WAIT_CMD :
        self.rx_packet.cmd = rx_data
        self.rx_packet.check_sum ^= rx_data
        self.state = self.CMD_STATE_WAIT_DIR
        
      case self.CMD_STATE_WAIT_DIR:
        self.rx_packet.dir = rx_data
        self.rx_packet.check_sum ^= rx_data
        self.state = self.CMD_STATE_WAIT_ERROR
        
      case self.CMD_STATE_WAIT_ERROR:
        self.rx_packet.error = rx_data
        self.rx_packet.check_sum ^= rx_data
        self.rx_packet.length = 0
        self.rx_packet.buffer = []
        self.index = 0
        self.state = self.CMD_STATE_WAIT_LENGTH_L
        
      case self.CMD_STATE_WAIT_LENGTH_L:
        self.rx_packet.length = rx_data
        self.rx_packet.check_sum ^= rx_data
        self.state = self.CMD_STATE_WAIT_LENGTH_H
        
      case self.CMD_STATE_WAIT_LENGTH_H:
        self.rx_packet.length |= rx_data << 8
        self.rx_packet.check_sum ^= rx_data
        if(self.rx_packet.length > 0):
          self.rx_packet.buffer = []
          self.state = self.CMD_STATE_WAIT_DATA
        else:
          self.state = self.CMD_STATE_WAIT_CHECKSUM
      
      case self.CMD_STATE_WAIT_DATA:
        self.rx_packet.buffer.append(rx_data)
        self.rx_packet.check_sum ^= rx_data
        self.index += 1
        if(self.index == self.rx_packet.length):
          self.state = self.CMD_STATE_WAIT_CHECKSUM
        else:
          self.state = self.CMD_STATE_WAIT_DATA
          
      case self.CMD_STATE_WAIT_CHECKSUM:
        self.rx_packet.check_sum_recv = rx_data
        self.state = self.CMD_STATE_WAIT_ETX
      
      case self.CMD_STATE_WAIT_ETX:
        if(rx_data == self.CMD_EXT):
          if(self.rx_packet.check_sum == self.rx_packet.check_sum_recv):
            ret = True
        self.state = self.CMD_STATE_WAIT_STX  
    return ret
        
        
  def cmdSendCmd(self, cmd, data, length):
    self.tx_packet.buffer = []
    self.tx_packet.buffer.append(self.CMD_STX)
    self.tx_packet.buffer.append(cmd)
    self.tx_packet.buffer.append(self.CMD_DIR_M_TO_S)
    self.tx_packet.buffer.append(self.CMD_OK)
    self.tx_packet.buffer.append((length >> 0) & 0xFF)
    self.tx_packet.buffer.append((length >> 8) & 0xFF)
    
    for i in range(length):
      self.tx_packet.buffer.append(data[i])
    
    checksum = 0
    
    for i in range(1, length + 6, 1):
      checksum ^= self.tx_packet.buffer[i]
      
    self.tx_packet.buffer.append(checksum)
    self.tx_packet.buffer.append(self.CMD_EXT)
    self.uart.write(self.tx_packet.buffer)
    
  
  def cmdSendResp(self, cmd, err_code, data, length):
    self.tx_packet.buffer.append(self.CMD_STX)
    self.tx_packet.buffer.append(cmd)
    self.tx_packet.buffer.append(self.CMD_DIR_M_TO_S)
    self.tx_packet.buffer.append(err_code)
    self.tx_packet.buffer.append((length >> 0) & 0xFF)
    self.tx_packet.buffer.append((length >> 8) & 0xFF)
    
    for i in range(length):
      self.tx_packet.buffer.append(data[i])
    
    checksum = 0
    
    for i in range(length + 5):
      i+=1
      checksum ^= self.tx_packet.buffer[i]
      
    self.tx_packet.buffer.append(checksum)
    self.tx_packet.buffer.append(self.CMD_EXT)
    
    self.uart.write(self.tx_packet.buffer)
  
  def cmdSendCmdRxResp(self, cmd, data, length, timout):
    ret = False
    pretime = 0
    
    self.cmdSendCmd(cmd, data, length)
    
    pretime = millis()

    while True:
      if(self.cmdReceivePacket() == True):
        ret = True
        break
      
      if(millis() - pretime > timout):
        break
    
    return ret
    
  