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
from core import *

# Download a project
def downloadProject(id):
    id = str(id)
    # Get ID from URLs
    if "soundtrap.com" in id:
        id = urlparse(id).path.rstrip('/').split('/')[-1]
    dlurl = "https://www.soundtrap.com/stream/" + id + "/s." + format
    apiurl = "https://www.soundtrap.com/api/project/getProject1/?id=" + id
    # Get project data
    r = s.head(apiurl)
    if r.status_code == 404:
        r = s.get(apiurl)
        error = r.json()
        message = error["error_message"]
        print(Style.BRIGHT + Fore.RED + "(!) " + message + Style.RESET_ALL)
    elif r.status_code == 409:
        r = s.get(apiurl)
        error = r.json()
        title = error["name"]
        message = error["message"]        
        print(Style.BRIGHT + Fore.RED + "(!) " + title + ": " + message + Style.RESET_ALL)
    else:
        r = s.get(apiurl)
        project = r.json()
        owner = project["owner"]
        data = project["data"]
        data = json.loads(data)
        title = project["title"]
        ctitle = re.sub('\<|\>|\:|\"|\/|\\|\||\?|\*', '', title)
        artist = owner["fullName"]
        date = str(project["lastUpdated"])[:-3]
        date = int(date)
        date = datetime.fromtimestamp(date).isoformat()[:-9]
        bpm = str(data["bpm"])
        key = data["key"]
        # Download the project
        print(Style.BRIGHT + Fore.WHITE + "Downloading '" + Fore.GREEN + title + Fore.WHITE + "' [" + Fore.GREEN + id + Fore.WHITE + "] by '" + Fore.GREEN + artist + Fore.WHITE + "'..." + Style.RESET_ALL)
        if os.path.isfile(dlpath + "/" + ctitle + "." + format):
            print(Style.BRIGHT + Fore.RED + "(!) This project is already downloaded." + Style.RESET_ALL)
        else:
            r = s.head(dlurl)
            # If stream doesn't exist
            if r.status_code == 404:
                print(Style.BRIGHT + Fore.RED + "(!) This project can't be downloaded." + Style.RESET_ALL)
            # If stream is unaccessible
            elif r.status_code == 409:
                r = s.get(dlurl)
                error = r.json()
                title = error["name"]
                message = error["message"]        
                print(Style.BRIGHT + Fore.RED + "(!) " + title + ": " + message + Style.RESET_ALL)
            else:
                r = s.get(dlurl, stream=True)
                total = int(r.headers.get('content-length', 0))
                with open(dlpath + "/" + ctitle + "." + format, "wb") as file, tqdm(
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
                with open(dlpath + "/" + ctitle + "." + format, encoding="cp850") as f:
                    deen = str(f.readlines())
                    invalids = ["error", "message", "details", "found"]
                    if re.compile('|'.join(invalids),re.IGNORECASE).search(deen):
                        print(Style.BRIGHT + Fore.WHITE + "[" + Fore.RED + "File Validator" + Fore.WHITE + "] Not a valid audio file." + Style.RESET_ALL)
                        invalidfile = True
                    else:
                        print(Style.BRIGHT + Fore.WHITE + "[" + Fore.GREEN + "File Validator" + Fore.WHITE + "] File OK." + Style.RESET_ALL)
                        invalidfile = False
                if invalidfile == True:
                    if dif == "y":
                        os.remove(dlpath + "/" + ctitle + "." + format)
                elif invalidfile == False:
                    # MP3 Tags
                    if format == "mp3":
                        audio = mutagen.File(dlpath + "/" + ctitle + ".mp3", easy=True)
                        audio.add_tags()
                        audio["title"] = title
                        audio["artist"] = artist
                        audio["date"] = date
                        audio["bpm"] = bpm
                        audio.save(dlpath + "/" + ctitle + ".mp3",v1=0)
                    # Automated conversion to FLAC
                    if format == "wav":
                        if c2f == "y":
                            song = AudioSegment.from_wav(dlpath + "/" + ctitle + ".wav")
                            if os.path.isfile(dlpath + "/" + ctitle + ".flac"):
                                print(Style.BRIGHT + Fore.RED + "(!) This project is already converted." + Style.RESET_ALL)
                            else:
                                song.export(dlpath + "/" + ctitle + ".flac", format="flac")
                                # FLAC Tags
                                audio = FLAC(dlpath + "/" + ctitle + ".flac")
                                audio["title"] = title
                                audio["artist"] = artist
                                audio["year"] = date
                                audio["bpm"] = bpm
                                audio["key"] = key
                                audio.save()
                                # Remove WAV after conversion
                                if dac == "y":
                                    os.remove(dlpath + "/" + ctitle + ".wav")

# Download a folder
def downloadFolder(id):
    global dlpath
    try:
        id = int(id)
        id = id - 1
        apiurl = "https://www.soundtrap.com/api/folder/getFolders1/?offset=0&count=999&order=ASC"
        r = s.head(apiurl)
        if r.status_code == 200:
            r = s.get(apiurl)
            folders = r.json()
            folder  = folders[id]
            projectIds = folder["projectIds"]
            foldername = folder["name"]
            cfoldername = re.sub('\<|\>|\:|\"|\/|\\|\||\?|\*', '', foldername)
            dlpath = dlpath + "/" + cfoldername
            if not os.path.exists(dlpath):
                os.makedirs(dlpath)
            print(Style.BRIGHT + Fore.WHITE + "Downloading folder '" + Fore.GREEN + foldername + Fore.WHITE + "' [" + Fore.GREEN + str(id + 1) + Fore.WHITE + "]..." + Style.RESET_ALL)
            for projectId in projectIds:
                downloadProject(projectId)
            print(Style.BRIGHT + Fore.WHITE + "Downloading folder '" + Fore.GREEN + foldername + Fore.WHITE + "' finished." + Style.RESET_ALL)
            dlpath = path + "/" + (config["dlpath"])
        else:
            print(Style.BRIGHT + Fore.RED + "(!) API couldn't be accessed." + Style.RESET_ALL)
    except ValueError:
        print(Style.BRIGHT + Fore.RED + "(!) Folder ID has to be a integer.")
    except IndexError:
        print(Style.BRIGHT + Fore.RED + "(!) Folder doesn't exist.")
