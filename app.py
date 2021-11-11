from download import *
if format not in ["mp3", "wav", "ogg"]:
    print("Invalid format '" + format + "', only MP3, WAV and OGG can be downloaded from Soundtrap.")
else:
    print("")       
    print(Fore.GREEN + "       ((((                 (((((                 ((((" + Style.RESET_ALL)  
    print(Fore.GREEN + Style.BRIGHT + "     ((((((                 (((((                 ((((((" + Style.RESET_ALL)
    print(Fore.GREEN + "   ((((((                   (((((                   ((((((" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + "  ((((((                    (((((                    ((((((" + Style.RESET_ALL)
    print(Fore.GREEN + " (((((                      (((((                     ((((((" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + " (((((                      (((((                      (((((" + Style.RESET_ALL)
    print(Fore.GREEN + "(((((      (((((((((((((((((((((((((((((((((((((((     (((((" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + "(((((       (((((((((((((((((((((((((((((((((((((      (((((" + Style.RESET_ALL)
    print(Fore.GREEN + " (((((        (((((((((((((((((((((((((((((((((        (((((" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + " ((((((          (((((((((((((((((((((((((((          ((((((" + Style.RESET_ALL)
    print(Fore.GREEN + "  ((((((           (((((((((((((((((((((((           ((((((" + Style.RESET_ALL) 
    print(Fore.GREEN + Style.BRIGHT + "   (((((((            (((((((((((((((((            ((((((" + Style.RESET_ALL)  
    print(Fore.GREEN + "     ((((((             (((((((((((((             ((((((" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + "       /((                 (((((((                 ((" + Style.RESET_ALL)    
    print(Fore.GREEN + "                             (((" + Style.RESET_ALL)                
    print("")
    print(Fore.GREEN + "————————————" + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + "1" + Fore.GREEN + Style.BRIGHT + " > " + Fore.WHITE + Style.BRIGHT + "Project" + Style.RESET_ALL)
    print(Fore.WHITE + Style.BRIGHT + "2" + Fore.GREEN + Style.BRIGHT + " > " + Fore.WHITE + Style.BRIGHT + "Folder" + Style.RESET_ALL)
    print(Fore.GREEN + "————————————" + Style.RESET_ALL)
    instatus()
    option = input(Fore.WHITE + Style.BRIGHT + "Choose: " + Style.RESET_ALL)
    if option == "1":
        while True:
            id = input(Fore.GREEN + "♫" + Fore.WHITE + Style.BRIGHT + " Project ID: " + Style.RESET_ALL)
            downloadProject(id)
    if option == "2":
        while True:
            fid = int(input(Fore.GREEN + "♫" + Fore.WHITE + Style.BRIGHT + " Folder ID: " + Style.RESET_ALL))
            downloadFolder(fid)
    else:
        exit()
