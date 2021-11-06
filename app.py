from download import *
if format not in ["mp3", "wav", "ogg"]:
    print("Invalid format '" + format + "', only MP3, WAV and OGG can be downloaded from Soundtrap.")
else:
    print("")       
    print("       ((((                 (((((                 ((((")  
    print("     ((((((                 (((((                 ((((((")
    print("   ((((((                   (((((                   ((((((")
    print("  ((((((                    (((((                    ((((((")
    print(" (((((                      (((((                     ((((((")
    print(" (((((                      (((((                      (((((")
    print("(((((      (((((((((((((((((((((((((((((((((((((((     (((((")
    print("(((((       (((((((((((((((((((((((((((((((((((((      (((((")
    print(" (((((        (((((((((((((((((((((((((((((((((        (((((")
    print(" ((((((          (((((((((((((((((((((((((((          ((((((")
    print("  ((((((           (((((((((((((((((((((((           ((((((") 
    print("   (((((((            (((((((((((((((((            ((((((")  
    print("     ((((((             (((((((((((((             ((((((")
    print("       /((                 (((((((                 ((")    
    print("                             (((")                
    print("")
    print("————————————")
    print("1 > Project")
    print("2 > Folder")
    print("————————————")
    instatus()
    option = input("Choose: ")
    if option == "1":
        while True:
            id = input("♫ Project ID: ")
            if id == "":
                print("Invalid Project ID.")
            else:
                downloadProject(id)
    if option == "2":
        while True:
            psid = int(input("♫ Folder ID: "))
            if psid == "":
                print("Invalid Folder ID.")
            else:
                downloadFolder(psid)
    else:
        exit()
