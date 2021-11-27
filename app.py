from download import *

os.system('cls')

# Nagging if the format can't be downloaded.
if format not in ["mp3", "wav", "ogg"]:
    print(Style.BRIGHT + Fore.RED + "(!) Invalid format '" + format + "', only MP3, WAV and OGG can be downloaded from Soundtrap." + Style.RESET_ALL)

# Information
appName = "Soundtap"
appVer = "2.1"
appAuthor = "wwwawww"
appRepo = "soundtap"
appSite = "https://github.com/" + appAuthor + "/" + appRepo

# Logged in status
def instatus():
    apiurl = "https://www.soundtrap.com/api/user/getMe1/"
    caniaccessit = s.head(apiurl)
    if caniaccessit.status_code == 200:
        rapi = s.get(apiurl)
        me = rapi.json()
        username = (me["username"])
        subscription = (me["planTier"])
        subscription = (subscription["name"])
        subscription = subscription[0].upper()+subscription[1:]
        print(Style.BRIGHT + Fore.WHITE + "Logged in as '" + Fore.GREEN + username + Fore.WHITE + "' (" + Fore.GREEN + subscription + Fore.WHITE + ")" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + Fore.RED + "(!) You aren't logged in" + Style.RESET_ALL)

# Checks for updates
def update():
    r = requests.get("https://api.github.com/repos/" + appAuthor + "/" + appRepo + "/releases/latest")
    global uUrl, uV, uDate, uDesc
    uUrl = (r.json()["html_url"])
    uV = (r.json()["tag_name"])
    uDate = (r.json()["published_at"])[:-10]
    uDate = datetime.strptime(uDate, "%Y-%m-%d").strftime("%d.%m.%Y")
    uDesc = (r.json()["body"])
    if appVer != uV:
        print(Style.BRIGHT + Fore.YELLOW + "(+) Update " + uV + " is available at " + appSite + Style.RESET_ALL)

def line():
    print(Fore.WHITE + ")" + Fore.GREEN + "————————————" + Fore.WHITE + "(" + Style.RESET_ALL)
def option(number, label):
    print(Style.BRIGHT + Fore.WHITE + number + Fore.GREEN + " > " + Fore.WHITE + label + Style.RESET_ALL)
def ctext1(i):
    print(Fore.WHITE + i + Style.RESET_ALL)
def ctext2(i):
    print(Style.BRIGHT + Fore.GREEN + i + Style.RESET_ALL)  
def choose():
    while True:
        option = input(Style.BRIGHT + Fore.WHITE + "Choose: " + Style.RESET_ALL)
        if option == "1":
            while True:
                id = input(Fore.GREEN + "♫" + Style.BRIGHT + Fore.WHITE + " Project ID: " + Style.RESET_ALL)
                downloadProject(id)
        elif option == "2":
            while True:
                try:
                    id = int(input(Fore.GREEN + "♫" + Style.BRIGHT + Fore.WHITE + " Folder ID: " + Style.RESET_ALL))
                    downloadFolder(id)
                except ValueError:
                    print(Style.BRIGHT + Fore.RED + "(!) Folder ID must be a integer.")
        elif option == "+":
            print(Style.BRIGHT + Fore.YELLOW + "———— " + Fore.WHITE + "Update information " + Fore.YELLOW + "————————————————————————")
            print(Fore.WHITE + appName + " " + Fore.YELLOW + uV + Fore.WHITE + " (" + Fore.YELLOW + uDate + Fore.WHITE + ")")
            print(Fore.WHITE + "Description:\n" + Fore.YELLOW + uDesc)
            print(Fore.WHITE + "You can download this update at: " + Fore.YELLOW + uUrl)
            print(Fore.YELLOW + "————————————————————————————————————————————————" + Style.RESET_ALL)
        else:
            exit()

print("")
ctext1("       ((((                 (())                 ))))")
ctext2("     ((((((                 (())                 ))))))")
ctext1("   ((((((                   (())                   ))))))")
ctext2("  ((((((                    (())                    ))))))")
ctext1(" (((((                      (())                      )))))")
ctext2(" (((((                      (())                      )))))")
ctext1("(((((      ((((((((((((((((((()))))))))))))))))))      )))))")
ctext2("(((((       (((((((((((((((((())))))))))))))))))       )))))")
ctext1(" (((((        (((((((((((((((())))))))))))))))        )))))")
ctext2(" ((((((          ((((((((((((()))))))))))))          ))))))")
ctext1("  ((((((           ((((((((((()))))))))))           ))))))")
ctext2("   ((((((             (((((((())))))))            ))))))")
ctext1("     ((((((             (((((())))))             ))))))")
ctext2("        ((                 ((()))                 ))")
ctext1("                             ()")
print("")
print(Style.BRIGHT + Fore.WHITE + appName + " " + Fore.GREEN + appVer + Style.RESET_ALL)
line()
option("1", "Project")
option("2", "Folder")
line()
instatus()
update()
choose()
