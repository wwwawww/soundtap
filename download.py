# Depencies
import os
import http.cookiejar
import datetime
from datetime import datetime
import requests
import time
import mutagen
from mutagen import *
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import json
from tqdm import tqdm
from pydub import AudioSegment
from pathlib import Path
import re
from urllib.parse import urlparse
from colorama import Fore, Back, Style

os.system('cls')

path = str(Path(__file__).parent.absolute())

if not os.path.exists(path + "/config.json"):
    f = open(path + "/config.json", 'a+')
    f.write('{"dlpath": "Downloads", "session": "", "format": "wav", "c2f": "n", "dac": "n"}')
    f.close()
    
with open(path + "/config.json") as f:
    config = json.load(f)
    jbsess = (config["session"])
    format = (config["format"])
    c2f = (config["c2f"])
    dac = (config["dac"])
    dlpath = path + "/" + (config["dlpath"])

if not os.path.exists(dlpath):
    os.makedirs(dlpath)

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
        print(Fore.WHITE + Style.BRIGHT + "Logged in as '" + Fore.GREEN + Style.BRIGHT + username + Fore.WHITE + Style.BRIGHT + "' (" + Fore.GREEN + Style.BRIGHT + subscription + " subscription" + Fore.WHITE + Style.BRIGHT + ")" + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "(!) You aren't logged in" + Style.RESET_ALL)
    
# Session
s = requests.session()
s.cookies.set("jb_SESSION", jbsess, domain="soundtrap.com")
s.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Accept-Language": "en-US,en"
}

# Download a project
def downloadProject(id):
    if "soundtrap.com" in id:
        id = urlparse(id).path.rstrip('/').split('/')[-1]
    dlurl = "https://www.soundtrap.com/stream/" + id + "/s." + format
    # Using /stream/ instead of /download/ to get WAV for free users.
    # Works as of November 2021, first discovered late October.
    # If it stops working, change to: "https://www.soundtrap.com/download/" + id + "/?format=" + format
    apiurl = "https://www.soundtrap.com/api/project/getProject1/?id=" + id
    caniaccessit = s.head(apiurl)
    caniaccessit.status_code
    if caniaccessit.status_code == 404:
        m = s.get(apiurl)
        m = m.json()
        ms = (m["error_message"])
        print(Fore.RED + Style.BRIGHT + "(!) " + ms + Style.RESET_ALL)
    elif caniaccessit.status_code == 409:
        m = s.get(apiurl)
        m = m.json()
        mn = (m["name"])
        ms = (m["message"])        
        print(Fore.RED + Style.BRIGHT + "(!) " + mn + ": " + ms + Style.RESET_ALL)
    else:
        rapi = s.get(apiurl)
        pi = rapi.json()
        title = (pi["title"])
        ftitle = re.sub('\<|\>|\:|\"|\/|\\|\||\?|\*', '', title)
        year = str((pi["lastUpdated"]))[:-3]
        year = int(year)
        year = datetime.fromtimestamp(year).isoformat()[:-9]
        pio = (pi["owner"])
        artist = (pio["fullName"])
        pid = (pi["data"])
        pid = json.loads(pid)
        bpm = (pid["bpm"])
        bpm = str(bpm)
        key = (pid["key"])
        print(Fore.WHITE + Style.BRIGHT + "Downloading '" + Fore.GREEN + Style.BRIGHT + title + Fore.WHITE + Style.BRIGHT + "' [" + Fore.GREEN + Style.BRIGHT + id + Fore.WHITE + Style.BRIGHT + "] by '" + Fore.GREEN + Style.BRIGHT + artist + Fore.WHITE + Style.BRIGHT + "'..." + Style.RESET_ALL)
        if os.path.isfile(dlpath + "/" + ftitle + "." + format):
            print(Fore.RED + Style.BRIGHT + "(!) This project is already downloaded." + Style.RESET_ALL)
        else:
            caniaccessit = s.head(dlurl)
            caniaccessit.status_code
            if caniaccessit.status_code == 404:
                print(Fore.RED + Style.BRIGHT + "(!) This project can't be downloaded." + Style.RESET_ALL)
            else:
                r = s.get(dlurl, stream=True)
                total = int(r.headers.get('content-length', 0))
                with open(dlpath + "/" + ftitle + "." + format, "wb") as file, tqdm(
                    desc=Fore.GREEN + Style.BRIGHT + title,
                    total=total,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for data in r.iter_content(chunk_size=1024):
                        size = file.write(data)
                        bar.update(size)
                print(Fore.GREEN + Style.BRIGHT + "Download finished." + Style.RESET_ALL)
                # MP3 Tags
                if format == "mp3":
                    audio = mutagen.File(dlpath + "/" + ftitle + ".mp3", easy=True)
                    audio.add_tags()
                    audio["title"] = title
                    audio["artist"] = artist
                    audio["date"] = year
                    audio["copyright"] = artist
                    audio["bpm"] = bpm
                    # I guess there is no key for this?
                    #audio["key"] = key
                    audio.save(dlpath + "/" + ftitle + ".mp3",v1=0)
                # Automated conversion to FLAC
                if format == "wav":
                    if c2f == "y":
                        song = AudioSegment.from_wav(dlpath + "/" + ftitle + ".wav")
                        if os.path.isfile(dlpath + "/" + ftitle + ".flac"):
                            print(Fore.RED + Style.BRIGHT + "(!) This project is already downloaded." + Style.RESET_ALL)
                        else:
                            song.export(dlpath + "/" + ftitle + ".flac", format="flac")
                            # FLAC Tags
                            audio = FLAC(dlpath + "/" + ftitle + ".flac")
                            audio["title"] = title
                            audio["artist"] = artist
                            audio["year"] = year
                            audio["copyright"] = artist
                            audio["bpm"] = bpm
                            audio["key"] = key
                            audio.save()
                            # Remove WAV after conversion
                            if dac == "y":
                                os.remove(dlpath + "/" + ftitle + ".wav")

# Download a folder
def downloadFolder(fid):
    pjscounter = int(0)
    fapiurl = "https://www.soundtrap.com/api/folder/getFolders1/?offset=0&count=999&order=ASC"
    caniaccessit = s.head(fapiurl)
    caniaccessit.status_code
    if caniaccessit.status_code == 200:
        try:
            rpsapi = s.get(fapiurl)
            fi = rpsapi.json()
            fip  = (fi[fid])
            fii = (fip["projectIds"])
            nop = (fip["numberOfProjects"])
            projectstitle = (fip["name"])
            fipr = (fii[pjscounter])
            fprojectstitle = re.sub('\<|\>|\:|\"|\/|\\|\||\?|\*', '', projectstitle)
            global dlpath
            dlpath = dlpath + "/" + fprojectstitle
            if not os.path.exists(dlpath):
                os.makedirs(dlpath)
            print(Fore.WHITE + Style.BRIGHT + "Downloading folder '" + Fore.GREEN + Style.BRIGHT + projectstitle + Fore.WHITE + Style.BRIGHT + "' [" + Fore.GREEN + Style.BRIGHT + str(fid) + Fore.WHITE + Style.BRIGHT + "]..." + Style.RESET_ALL)
            while pjscounter < nop:
                fipr = (fii[pjscounter])
                downloadProject(fipr)
                pjscounter += int(1)
            dlpath = path + "/" + (config["dlpath"])
        except IndexError:
            print(Fore.RED + Style.BRIGHT + "(!) This folder doesn't exist or is empty." + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "(!) Folders couldn't be accessed." + Style.RESET_ALL)
