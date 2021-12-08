import os
from colorama import Fore, Back, Style
from download import *
from core import *

def line():
    print(Fore.WHITE + ")" + Fore.GREEN + "————————————" + Fore.WHITE + "(" + Style.RESET_ALL)
def option(number, label):
    print(Style.BRIGHT + Fore.WHITE + number + Fore.GREEN + " > " + Fore.WHITE + label + Style.RESET_ALL)
def white(text):
    print(Style.BRIGHT + Fore.WHITE + text + Style.RESET_ALL)
def green(text):
    print(Style.BRIGHT + Fore.GREEN + text + Style.RESET_ALL)  
def choose():
    while True:
        option = input(Style.BRIGHT + Fore.WHITE + "Choose: " + Style.RESET_ALL)
        if option == "1":
            while True:
                id = input(Fore.GREEN + "♫" + Style.BRIGHT + Fore.WHITE + " Project ID: " + Style.RESET_ALL)
                downloadProject(id)
        elif option == "2":
            while True:
                id = input(Fore.GREEN + "♫" + Style.BRIGHT + Fore.WHITE + " Folder ID: " + Style.RESET_ALL)
                downloadFolder(id)
        else:
            exit()

os.system("cls")
print("")
white("       ((((                 (())                 ))))")
green("     ((((((                 (())                 ))))))")
white("   ((((((                   (())                   ))))))")
green("  ((((((                    (())                    ))))))")
white(" (((((                      (())                      )))))")
green(" (((((                      (())                      )))))")
white("(((((      ((((((((((((((((((()))))))))))))))))))      )))))")
green("(((((       (((((((((((((((((())))))))))))))))))       )))))")
white(" (((((        (((((((((((((((())))))))))))))))        )))))")
green(" ((((((          ((((((((((((()))))))))))))          ))))))")
white("  ((((((           ((((((((((()))))))))))           ))))))")
green("   ((((((             (((((((())))))))            ))))))")
white("     ((((((             (((((())))))             ))))))")
green("        ((                 ((()))                 ))")
white("                             ()")
print("")
print(Style.BRIGHT + Fore.WHITE + appName + " " + Fore.GREEN + appVer + Style.RESET_ALL)
line()
option("1", "Project")
option("2", "Folder")
line()
status()
choose()
