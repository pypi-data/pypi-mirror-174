from .cmd import CMD
from .boot import BOOT
import os
import colorama
import click

@click.command()
@click.option("--port", prompt = "Enter port", help="The name port")
@click.option("--baud", prompt = "Enter Baud rate", help="The Baud rate")
def main(port, baud):
    cmd = CMD(port, baud)
    cmd.init()
    cmd.open()
    while True:
      print(colorama.Fore.GREEN + "-------------------------------------")
      print("1. Led")
      print("2. BootLoader")
      print("3. Exit")
      print("-------------------------------------")
      option = option = input("Choose type:  ")
      
      match option:
        case "1":
          os.system('clear')
          led(cmd)
          
        case "2":
          os.system('clear')
          boot(cmd)
        
        case "3":
          print("Good bye!")
          break
          
        case _:
          print(colorama.Fore.RED + "Input invalid!")
          _ = input("Press anykey....")  
        
      os.system('clear')


def led(cmd):
  while True:
    print(colorama.Fore.GREEN + "-------------------LED TEST------------------")
    print("1. Led ON")
    print("2. Led OFF")
    print("3. Led Toggle")
    print("4. Exit")
    print("---------------------------------------------")
    option = input("Choose type:   ")
    if(option == "1"):
      if(cmd.cmdSendCmdRxResp(0x10, [1], 1, 1) == True):
        print(colorama.Fore.GREEN + "Led ON success!")
      else:
        print(colorama.Fore.RED + "Led ON Fail!")
    elif(option == "2"):
      if(cmd.cmdSendCmdRxResp(0x10, [2], 1, 1) == True):
        print(colorama.Fore.GREEN +  "Led OFF success!")
      else:
        print(colorama.Fore.RED + "Led OFF Fail!")
    elif(option == "3"):
      if(cmd.cmdSendCmdRxResp(0x10, [3], 1, 1) == True):
        print(colorama.Fore.GREEN +  "Led Toggle success!")
      else:
        print(colorama.Fore.RED + "Led Toggle Fail!")
    elif(option == "4"):
      os.system('clear')
      break
    else:
      print(colorama.Fore.RED + "Input invalid!")
    _ = input("Press anykey....")
    os.system('clear')
      

def boot(cmd):
  bootMCU = BOOT(cmd)
  while True:
    print(colorama.Fore.GREEN + "------------------- BOOT ------------------")
    print("1. Read BootLoader Version")
    print("2. Read BootLoader Name")
    print("3. Read Flash")
    print("4. Exit")
    print("-------------------------------------------")
    
    option = input("Choose type:   ")
    
    bootMCU.bootProcessCmd(option)
    
    if(option == "4"):
      break
    _ = input("Press anykey....")
    os.system('clear')
  
  
if __name__ == "__main__":
  main()