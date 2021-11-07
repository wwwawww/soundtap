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

path = str(Path(__file__).parent.absolute())
dlpath = path + "/Downloads"

if not os.path.exists(path + "/config.json"):
    f = open(path + "/config.json", 'a+')
    f.write('{"session": "","format": "wav","c2f": "n","dac": "n"}')
    f.close()

if not os.path.exists(dlpath):
    os.makedirs(dlpath)
    
with open(path + "/config.json") as f:
    config = json.load(f)
    jbsess = (config["session"])
    format = (config["format"])
    c2f = (config["c2f"])
    dac = (config["dac"])

def instatus():
    ts = s.head("https://www.soundtrap.com/api/conversation/getStatus1")
    if ts.status_code == 200:
        print("You are logged in.")
    else:
        print("You aren't logged in.")
    
# Session
s = requests.session()
s.cookies.set("jb_SESSION", jbsess, domain="soundtrap.com")
s.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Accept-Language": "en-US,en"
}

# Project
def downloadProject(id):
    if "soundtrap.com" in id:
        id = urlparse(id).path.rstrip('/').split('/')[-1]
    dlurl = "https://www.soundtrap.com/stream/" + id + "/s." + format
    # Using /stream/ instead of /download/ to get WAV for free users.
    apiurl = "https://www.soundtrap.com/api/project/getProject1/?id=" + id
    caniaccessit = s.head(apiurl)
    caniaccessit.status_code
    if caniaccessit.status_code == 404:
        print("Project wasn't found.")
    elif caniaccessit.status_code == 409:
        print("No access.")
    else:
        rapi = s.get(apiurl)
        pinfo = rapi.json()
        title = (pinfo["title"])
        ftitle = re.sub('\<|\>|\:|\"|\/|\\|\||\?|\*', '', title)
        year = str((pinfo["lastUpdated"]))[:-3]
        year = int(year)
        year = datetime.fromtimestamp(year).isoformat()[:-9]
        pinfo2 = (pinfo["owner"])
        artist = (pinfo2["fullName"])
        pinfo3 = (pinfo["data"])
        pinfo3 = json.loads(pinfo3)
        bpm = (pinfo3["bpm"])
        bpm = str(bpm)
        key = (pinfo3["key"])
        genre = (pinfo3["template_kind"])
        genre = genre[0].upper()+genre[1:]
        print("Downloading '" + title + "' [" + id + "] by '" + artist + "'...")
        if os.path.isfile(dlpath + "/" + ftitle + "." + format):
            print("This project is already downloaded.")
        else:
            r = s.get(dlurl, stream=True)
            total = int(r.headers.get('content-length', 0))
            with open(dlpath + "/" + ftitle + "." + format, "wb") as file, tqdm(
                desc=title,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in r.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)
            print("Download finished.")
            # MP3 Tags
            if format == "mp3":
                audio = mutagen.File(dlpath + "/" + ftitle + ".mp3", easy=True)
                audio.add_tags()
                audio["title"] = title
                audio["artist"] = artist
                audio["genre"] = genre
                #audio["year"] = year[:-6]
                # Fuck this shit since POS mutagen never works anyway
                audio["copyright"] = artist
                audio["bpm"] = bpm
                #audio["key"] = key
                audio.save(dlpath + "/" + ftitle + ".mp3",v1=0)
                # Automated conversion to FLAC
            if format == "wav":
                if c2f == "y":
                    song = AudioSegment.from_wav(dlpath + "/" + ftitle + ".wav")
                    if os.path.isfile(dlpath + "/" + ftitle + ".flac"):
                        print("This project is already downloaded.")
                    else:
                        song.export(dlpath + "/" + ftitle + ".flac", format="flac")
                        # FLAC Tags
                        audio = FLAC(dlpath + "/" + ftitle + ".flac")
                        audio["title"] = title
                        audio["artist"] = artist
                        audio["genre"] = genre
                        audio["year"] = year
                        audio["copyright"] = artist
                        audio["bpm"] = bpm
                        audio["key"] = key
                        audio.save()
                        # Remove WAV after conversion
                        if dac == "y":
                            os.remove(dlpath + "/" + ftitle + ".wav")

# Projects
def downloadFolder(psid):
    pjscounter = int(0)
    psapiurl = "https://www.soundtrap.com/api/folder/getFolders1/?offset=0&count=999&order=ASC"
    caniaccessit = s.head(psapiurl)
    caniaccessit.status_code
    if caniaccessit.status_code == 200:
        try:
            rpsapi = s.get(psapiurl)
            psinfo_all = rpsapi.json()
            psinfo_ps  = (psinfo_all[psid])
            psinfo_ids = (psinfo_ps["projectIds"])
            nop = (psinfo_ps["numberOfProjects"])
            projectstitle = (psinfo_ps["name"])
            psinfo_pr = (psinfo_ids[pjscounter])
            #dlpath = dlpath + projectstitle + "/"
            print("Downloading folder '" + projectstitle + "' [" + str(psid) + "]...")
            while pjscounter < nop:
                psinfo_pr = (psinfo_ids[pjscounter])
                downloadProject(psinfo_pr)
                pjscounter += int(1)
        except IndexError:
            print("This folder doesn't exist or is empty.")
    else:
        print("Folders couldn't be accessed.")
