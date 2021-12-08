import os
import http.cookiejar
import datetime
from datetime import datetime
import requests
import time
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from colorama import Fore, Back, Style

# App information
appName = "Soundtap"
appVer = "3.0"
appAuthor = "wwwawww"

# Gets the current path
path = str(Path(__file__).parent.absolute())

# If config.json doesn't exist -> create it
if not os.path.exists(path + "/config.json"):
    f = open(path + "/config.json", 'a+')
    # Default config.json
    f.write('{"dlpath": "", "session": "", "format": "wav", "c2f": "y", "dac": "y", "dif": "y"}')
    f.close()

# Get configuration
with open(path + "/config.json") as f:
    config = json.load(f)
    dlpath = path + "/" + (config["dlpath"])
    # Session to log in
    session = (config["session"])
    # Format to lowercase, won't work otherwise
    format = str.lower((config["format"]))
    # Conversion to FLAC
    c2f = (config["c2f"])
    # Delete WAV after conversion
    dac = (config["dac"])
    # Delete invalid files
    dif = (config["dif"])

# Nagging if the format can't be downloaded.
if format not in ["mp3", "wav", "ogg"]:
    print(Style.BRIGHT + Fore.RED + "(!) Format '" + format + "', can't be downloaded." + Style.RESET_ALL)

# Session
s = requests.session()
s.cookies.set("jb_SESSION", session, domain="soundtrap.com")
# Disguising the downloader as a normal user
s.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

# If download path doesn't exist -> create it
if not os.path.exists(dlpath):
    os.makedirs(dlpath)

# Logged in status, fetch username if possible
def status():
    apiurl = "https://www.soundtrap.com/api/user/getMe1/"
    r = s.head(apiurl)
    if r.status_code == 200:
        r = s.get(apiurl)
        me = r.json()
        username = (me["username"])
        subscription = (me["planTier"])
        subscription = (subscription["name"])
        subscription = subscription[0].upper()+subscription[1:]
        print(Style.BRIGHT + Fore.WHITE + "Logged in as '" + Fore.GREEN + username + Fore.WHITE + "' (" + Fore.GREEN + subscription + Fore.WHITE + ")" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + Fore.RED + "(!) You aren't logged in" + Style.RESET_ALL)
