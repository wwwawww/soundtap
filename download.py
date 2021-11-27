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

# If download path doesn't exist -> create it
if not os.path.exists(dlpath):
    os.makedirs(dlpath)
    
# Session
s = requests.session()
s.cookies.set("jb_SESSION", session, domain="soundtrap.com")
# Disguising the downloader as a normal user
s.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

# Download a project
def downloadProject(id):
    # Get ID from /studio/ URLs
    if "soundtrap.com" in id:
        id = urlparse(id).path.rstrip('/').split('/')[-1]
    # /stream/ to get WAV for free users.
    dlurl = "https://www.soundtrap.com/stream/" + id + "/s." + format
    apiurl = "https://www.soundtrap.com/api/project/getProject1/?id=" + id
    caniaccessit = s.head(apiurl)
    if caniaccessit.status_code == 404:
        m = s.get(apiurl)
        m = m.json()
        ms = (m["error_message"])
        print(Style.BRIGHT + Fore.RED + "(!) " + ms + Style.RESET_ALL)
    elif caniaccessit.status_code == 409:
        m = s.get(apiurl)
        m = m.json()
        mn = (m["name"])
        ms = (m["message"])        
        print(Style.BRIGHT + Fore.RED + "(!) " + mn + ": " + ms + Style.RESET_ALL)
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
        print(Style.BRIGHT + Fore.WHITE + "Downloading '" + Fore.GREEN + title + Fore.WHITE + "' [" + Fore.GREEN + id + Fore.WHITE + "] by '" + Fore.GREEN + artist + Fore.WHITE + "'..." + Style.RESET_ALL)
        if os.path.isfile(dlpath + "/" + ftitle + "." + format):
            print(Style.BRIGHT + Fore.RED + "(!) This project is already downloaded." + Style.RESET_ALL)
        else:
            caniaccessit = s.head(dlurl)
            caniaccessit.status_code
            if caniaccessit.status_code == 404:
                print(Style.BRIGHT + Fore.RED + "(!) This project can't be downloaded." + Style.RESET_ALL)
            elif caniaccessit.status_code == 409:
                m = s.get(dlurl)
                m = m.json()
                mn = (m["name"])
                ms = (m["message"])        
                print(Style.BRIGHT + Fore.RED + "(!) " + mn + ": " + ms + Style.RESET_ALL)
            else:
                r = s.get(dlurl, stream=True)
                total = int(r.headers.get('content-length', 0))
                with open(dlpath + "/" + ftitle + "." + format, "wb") as file, tqdm(
                    desc=Style.BRIGHT + Fore.WHITE + title,
                    total=total,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for data in r.iter_content(chunk_size=1024):
                        size = file.write(data)
                        bar.update(size)
                print(Style.BRIGHT + Fore.WHITE + "Download finished." + Style.RESET_ALL)
                # File Validation
                with open(dlpath + "/" + ftitle + "." + format, encoding="cp850") as f:
                    deen = str(f.readlines())
                    invalids = ["error", "message", "details"]
                    if re.compile('|'.join(invalids),re.IGNORECASE).search(deen):
                        print(Style.BRIGHT + Fore.WHITE + "[" + Fore.RED + "File Validator" + Fore.WHITE + "] Not a valid audio file." + Style.RESET_ALL)
                        invalidfile = True
                    else:
                        print(Style.BRIGHT + Fore.WHITE + "[" + Fore.GREEN + "File Validator" + Fore.WHITE + "] File OK." + Style.RESET_ALL)
                        invalidfile = False
                if invalidfile == True:
                    if dif == "y":
                        os.remove(dlpath + "/" + ftitle + "." + format)
                elif invalidfile == False:
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
                                print(Style.BRIGHT + Fore.RED + "(!) This project is already converted." + Style.RESET_ALL)
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
def downloadFolder(id):
    global dlpath
    pjscounter = int(0)
    apiurl = "https://www.soundtrap.com/api/folder/getFolders1/?offset=0&count=999&order=ASC"
    caniaccessit = s.head(apiurl)
    if caniaccessit.status_code == 200:
        try:
            rapi = s.get(apiurl)
            fi = rapi.json()
            fip  = (fi[id])
            fii = (fip["projectIds"])
            nop = (fip["numberOfProjects"])
            projectstitle = (fip["name"])
            fipr = (fii[pjscounter])
            fprojectstitle = re.sub('\<|\>|\:|\"|\/|\\|\||\?|\*', '', projectstitle)
            dlpath = dlpath + "/" + fprojectstitle
            if not os.path.exists(dlpath):
                os.makedirs(dlpath)
            print(Style.BRIGHT + Fore.WHITE + "Downloading folder '" + Fore.GREEN + projectstitle + Fore.WHITE + "' [" + Fore.GREEN + str(id) + Fore.WHITE + "]..." + Style.RESET_ALL)
            while pjscounter < nop:
                fipr = (fii[pjscounter])
                downloadProject(fipr)
                pjscounter += int(1)
            print(Style.BRIGHT + Fore.WHITE + "Downloading folder '" + Fore.GREEN + projectstitle + Fore.WHITE + "' finished." + Style.RESET_ALL)
            dlpath = path + "/" + (config["dlpath"])
        except IndexError:
            print(Style.BRIGHT + Fore.RED + "(!) This folder doesn't exist or is empty." + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + Fore.RED + "(!) Folders couldn't be accessed." + Style.RESET_ALL)
