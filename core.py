import os
from re import findall
from time import sleep
from shutil import rmtree
from datetime import datetime
from selenium import webdriver
from pyautogui import hotkey, typewrite

NAME = "Webpage Content Fetcher"
VERSION = "Release 2.0"
AUTHOR = "GitHub : MarcusPy"

WELCOME = f"""===========================
| {NAME} |\n| {AUTHOR}       |\n| {VERSION}             |
===========================
"""

os.system("cls")
print(WELCOME)
input("Do Not Touch Anything While The Tool Is Working, Press ENTER To Continue ")
os.system("cls")

# Constants, nothing to change except for DRIVER if using a different one (untested)
NOW = datetime.now()
CURRENTLY = NOW.strftime("%d-%b-%Y-%I;%M%p")
PATH_TEMP = os.path.dirname(__file__) + "\_temp"
PATH_TEMP_NEW = PATH_TEMP + "\\"
PATH_OUTPUT = os.path.dirname(__file__) + f"\{CURRENTLY}"

# Variables, feel free to edit them
variables = {
    # RegEx, each webpage will probably require a new one
    # Second one is for alternative pattern, if needed
    "P1" : r"\n\s{14}([0-9]{2}&nbsp;[0-9]{3}&nbsp;K=C4=8D)",
    "P2" : r"\n\s{14}([0-9]{1}&nbsp;[0-9]{3}&nbsp;K=C4=8D)",

    # Default delay between pyautogui actions to prevent issues, adjustable
    # Increase as needed if your PC is slow and you're experiencing file saving bugs
    "SLEEP" : 0.3,
    
    # Controls whether temporary files should be removed upon completion
    # It's recommended to keep this at False, that folder will anyway remove itself
    # Feel free to report errors along with the "_temp" and output folder
    "FORCE_CLEAN" : False
}

# Assign the variables for the sake of readability later on
P1 = variables["P1"]
P2 = variables["P2"]
SLEEP = variables["SLEEP"]
FORCE_CLEAN = variables["FORCE_CLEAN"]

errors = 0

def logger(*data):
    for _ in range(len(data)):
        print(f"> {data[_]}")

    with open(PATH_OUTPUT + "\Log.txt", "a") as log:
        now = datetime.now()
        now = now.strftime(f"[%Hh:%Mm:%Ss] : ")
        for _ in range(len(data)):
            log.write(f"{now}{data[_]}\n")

# Don't clutter the working directory, make a temporary one
try:
    os.mkdir(PATH_OUTPUT)
except FileExistsError:
    rmtree(PATH_OUTPUT)
    os.mkdir(PATH_OUTPUT)
finally:
    try:
        os.mkdir(PATH_TEMP)
    except FileExistsError:
        rmtree(PATH_TEMP)
        os.mkdir(PATH_TEMP)

urls = {
    "iPhone 13 Pro Max 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-256gb-alpine-green-a-pouzity-p-140126",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-256gb-alpine-green-pouzite-p-140127",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-256gb-alpine-green-c-pouzity-p-140128"
    },
    "iPhone 11 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-128gb-black-a-pouzity-p-103704",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-128gb-black-pouzite-p-103705",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-128gb-black-c-pouzity-p-103706"
    }
}

PHONES = len(urls.keys()) * 3

links = []
with open(PATH_OUTPUT + "\Links.txt", "w") as link:
    for k1 in urls.keys():
        link.write(f"{k1}:\n")
        for k2, v2 in urls[k1].items():
            links.append(v2)
            if k2 == "C":
                link.write(f"    {k2} : {v2}\n\n")
            else:
                link.write(f"    {k2} : {v2}\n")

abc, names = [], []
def downloader(retry:str=""):
    PATH_DRIVER = os.path.dirname(__file__) + "\msedgedriver"
    DRIVER = webdriver.Edge(executable_path=PATH_DRIVER)
    times = 0
    name = ""
    for k1 in urls.keys():
        name = k1 + " - "
        for k2, v2 in urls[k1].items():
            name += k2
            if len(retry) > 0:
                logger("Retrying To Download")
                DRIVER.get(retry)
                now = datetime.now()
                name = now.strftime("%f")
                _name = name
            else:
                DRIVER.get(v2)
                names.append(name)
                abc.append(k2)
                _name = name
            sleep(1)
            hotkey('ctrl', 's')
            sleep(SLEEP)
            typewrite(name)
            if times == 0: # Needed only once so that OS remembers last choices
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('right')
                sleep(SLEEP)
                hotkey('pageup')
                sleep(SLEEP)
                hotkey('w')
                sleep(SLEEP)
                hotkey('enter')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('enter')
                sleep(SLEEP)
                typewrite(PATH_TEMP)
                sleep(SLEEP)
                hotkey('enter')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
                sleep(SLEEP)
                hotkey('tab')
            sleep(SLEEP)
            hotkey('enter')
            sleep(SLEEP)
            if len(retry) > 0:
                return _name
            name = name[:-1]
            times += 1
            logger(f"[{times}/{PHONES}] Files Obtained")
        
    logger(f"Download Of [{times}] Files Complete")
    logger(names)
    #input("Debug Pause 1 ")

# Attempt to redownload and search, or alternativaly accept the error
def redownloader(i, file_name):
    global errors
    logger(f"Redownloading: {file_name}")
    retry = links[i]
    logger(f"Link: {retry}")
    _name = downloader(retry=retry)
    rnd_name = _name + ".mhtml"
    _name = PATH_TEMP_NEW + _name + ".mhtml"
    #input("Debug Pause 2")
    try:
        with open(_name, "r") as retried:
            _data = retried.read()
            _found = findall(P1, _data)
            if len(_found) == 0:
                _found = findall(P2, _data)
            if len(_found) == 1:
                result = _found[0]
                result = result.replace("&nbsp;", " ", 1)
                result = result.replace("&nbsp;K=C4=8D", "")
            elif len(_found) == 0:
                logger(f"Aborting, Still No Matching Data Was Found: {rnd_name}")
                result = "Error, Unable To Fetch Data Automatically"
                errors += 1
            elif len(_found) > 1:
                result = f"Aborting, Still More Than 1 Match Was Found: {_found} in {rnd_name}"
                result = result.replace("&nbsp;", " ")
                result = result.replace("K=C4=8D", "")
                logger(result)
                result = "Error, Unable To Fetch Data Automatically"
                errors += 1
    except FileNotFoundError:
        logger(f"Aborting, File Still Not Found: {rnd_name}")
        result = "Error, Unable To Fetch Data Automatically"
        errors += 1
    
    return result

# If this errors out, it calls redownloader to retry
def finder(i, temp_name, file_name):
    try:
        with open(temp_name, "r") as temp:
            data = temp.read()
            found = findall(P1, data)
            if len(found) == 0:
                found = findall(P2, data)
            if len(found) == 1:
                result = found[0]
                result = result.replace("&nbsp;", " ", 1)
                result = result.replace("&nbsp;K=C4=8D", "")
            elif len(found) == 0:
                logger(f"No Matching Data Was Found: {file_name}")
                result = redownloader(i, file_name)
            elif len(found) > 1:
                result = f"Found More Than 1 Match: {found} in {file_name}"
                result = result.replace("&nbsp;", " ")
                result = result.replace("K=C4=8D", "")
                logger(result)
                result = redownloader(i, file_name)
    except FileNotFoundError:
        logger(f"File Not Found: {file_name}")
        result = redownloader(i, file_name)
    
    return result

def core():
    downloader()
    headers = list(urls.keys())
    header = 0
    with open(PATH_OUTPUT + "\Prices.txt", "w") as cost:
        cost.write(f"{headers[0]}:\n")
        for _ in range(len(names)):
            file_name = f"'{names[_]}.mhtml'"
            temp_name = PATH_TEMP_NEW + names[_] + ".mhtml"
            result = finder(_, temp_name, file_name)
            if abc[_] == "C":
                cost.write(f"    {abc[_]} : {result}\n\n")
                try:
                    header += 1
                    cost.write(f"{headers[header]}:\n")
                except IndexError:
                    logger("Index OoB Reached")
                    if FORCE_CLEAN or errors == 0:
                        logger("Removing Temp Files...")
                        rmtree(PATH_TEMP) # Remove our temporary files to free up space
                        break
                    elif errors > 1:
                        break
            else:
                cost.write(f"    {abc[_]} : {result}\n")

core()

logger(f"Operation Finished, Output Located In {PATH_OUTPUT}")
if errors > 0:
    logger(f"Unsolved Errors: [{errors}], Check Logs For More Info")
