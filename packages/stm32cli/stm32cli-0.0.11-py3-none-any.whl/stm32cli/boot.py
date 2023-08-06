from .cmd import CMD

class BOOT:
  BOOT_CMD_READ_BOOT_VERSION =      0x00
  BOOT_CMD_READ_BOOT_NAME    =      0x01
  BOOT_CMD_READ_FIRM_VERSION =      0x02
  BOOT_CMD_READ_FIRM_NAME    =      0x03
  BOOT_CMD_FLASH_ERASE       =      0x04
  BOOT_CMD_FLASH_WRITE       =      0x05
  BOOT_CMD_FLASH_READ        =      0x06
  BOOT_CMD_JUMP_TO_FW        =      0x08

  BOOT_CMD_TAG_ERASE         =      0x10
  BOOT_CMD_TAG_WRITE         =      0x11
  BOOT_CMD_TAG_READ          =      0x12
  BOOT_CMD_TAG_VERIFY        =      0x13


  BOOT_CMD_UPDATE_ERASE      =      0x20
  BOOT_CMD_UPDATE_WRITE      =      0x21
  BOOT_CMD_UPDATE_READ       =      0x22
  BOOT_CMD_UPDATE_FW         =      0x24

  
  def __init__(self, cmd):
    self.cmd = cmd
  
  def bootProcessCmd(self, command):
    match command:
      case "1":
        if(self.cmd.cmdSendCmdRxResp(self.BOOT_CMD_READ_BOOT_VERSION, [], 0, 1) == True):
          version = ""
          for char in self.cmd.rx_packet.buffer:
            version+= chr(char)
          print(f"BootLoader Version: {version}")
        else:
          print(f"Read BootLoader Version Fail!")

      case "2":
        if(self.cmd.cmdSendCmdRxResp(self.BOOT_CMD_READ_BOOT_NAME, [], 0, 1) == True):
          name = ""
          for char in self.cmd.rx_packet.buffer:
            name+= chr(char)
          print(f"BootLoader Name: {name}")
        else:
          print(self.cmd.rx_packet.buffer)
          print(f"Read BootLoader Name Fail!")

      case "3":
        addr = input("Input Address (ex: 0x8000000): ")
        length = input("Input Length (ex: 1024)      : ")
        addr = int(addr, 16)
        length = int(length)
        data = [addr >> 0 & 0xFF, addr >> 8 & 0xFF,addr >> 16 & 0xFF,addr >> 24 & 0xFF, length >> 0 & 0xFF, length >> 8 & 0xFF, length >> 16 & 0xFF, length >> 24 & 0xFF]
        if(self.cmd.cmdSendCmdRxResp(self.BOOT_CMD_FLASH_READ, data, len(data), 3) == True):
          print(f"Flash Data:")
          data = []
          for i in range(0, len(self.cmd.rx_packet.buffer), 4):
            if((i+4) > len(self.cmd.rx_packet.buffer)):
              data.append(self.cmd.rx_packet.buffer[i])
              for j in range(1, (self.cmd.rx_packet.buffer)%4, 1):
                data[-1] |= self.cmd.rx_packet.buffer[i] << 8*i
            else:
              data.append((self.cmd.rx_packet.buffer[i]) << 0)
              data[-1] |= (self.cmd.rx_packet.buffer[i+1]) << 8
              data[-1] |= (self.cmd.rx_packet.buffer[i+2]) << 16
              data[-1] |= (self.cmd.rx_packet.buffer[i+3]) << 24
              
          for i in range(0, len(data), 4):
            if((i+4) > len(data)):
              for j in range(len(data)%4):
                print("{0}: {1}\r\n".format(hex((addr + 32*i)), data[j]))
            else:
              print("{0}: {1} | {2} | {3} | {4}\r\n".format(hex((addr + 32*i)), hex(data[i]), hex(data[i+1]), hex(data[i+2]), hex(data[i+3])))  
          
        else:
          print(f"Read Flash Fail!")
      
      case self.BOOT_CMD_READ_FIRM_NAME:
        pass

      case self.BOOT_CMD_FLASH_ERASE:
        pass

      case self.BOOT_CMD_FLASH_WRITE:
        pass

      case self.BOOT_CMD_FLASH_READ:
        pass

      case self.BOOT_CMD_JUMP_TO_FW:
        pass

      case self.BOOT_CMD_TAG_READ:
        pass

      case self.BOOT_CMD_TAG_WRITE:
        pass

      case self.BOOT_CMD_TAG_VERIFY:
        pass

      case self.BOOT_CMD_TAG_ERASE:
        pass

      case self.BOOT_CMD_UPDATE_ERASE:
        pass

      case self.BOOT_CMD_UPDATE_WRITE:
        pass

      case self.BOOT_CMD_UPDATE_READ:
        pass
      
      case self.BOOT_CMD_UPDATE_FW:
        pass
      
      
      case _:
        print("Input invalid")

