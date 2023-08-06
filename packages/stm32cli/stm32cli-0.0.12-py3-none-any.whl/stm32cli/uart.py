import serial
import sys

class UART:

  def __init__(self, ch, baud):
    try:
      self.ser = serial.Serial()
      self.ser.port = ch
      self.ser.baudrate = baud
    except:
      print("Input Ivalid, Please Check again!")
      sys.exit()
  
  def open(self):
    try:
      self.ser.open()
      print("UART open success!")
    except:
      print("Check your Port!")
      sys.exit()
    
  def available(self):
    ret = self.ser.in_waiting
    return ret
  
  def read(self):
    return self.ser.read(size=1)
  
  def write(self, data):
    ret =  self.ser.write(data)
    self.ser.flush()
    return ret
  
  def close(self):
    return self.ser.close()