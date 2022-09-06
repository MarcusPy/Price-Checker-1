import os
from re import findall
from time import sleep
from shutil import rmtree
from datetime import datetime
from selenium import webdriver
from pyautogui import hotkey, typewrite

NAME = "Webpage Content Fetcher"
VERSION = "Release 1.0"
AUTHOR = "GitHub : MarcusPy"

WELCOME = f"""===========================
| {NAME} |\n| {AUTHOR}       |\n| {VERSION}             |
===========================
"""

os.system("cls")
print(WELCOME)
input("\nDo Not Touch Anything While The Tool Is Working, Press ENTER To Continue ")
os.system("cls")

# constants, nothing to change except for DRIVER if using a different one, untested
NOW = datetime.now()
CURRENTLY = NOW.strftime("%d-%b-%Y-%I;%M%p")
PATH_TEMP = os.path.dirname(__file__) + "\_temp"
PATH_TEMP_NEW = PATH_TEMP + "\\"
PATH_OUTPUT = os.path.dirname(__file__) + f"\{CURRENTLY}"

# RegEx that works perfectly
P1 = r"\n\s{14}([0-9]{1}&nbsp;[0-9]{3}&nbsp;K=C4=8D)"
P2 = r"\n\s{14}([0-9]{2}&nbsp;[0-9]{3}&nbsp;K=C4=8D)"

# Default delay between pyautogui actions to prevent issues, adjustable
# Increase as needed if your PC is slow and you're experiencing file saving bugs
SLEEP = 0.3

def logger(*data):
    for _ in range(len(data)):
        print(f"> {data[_]}")

    with open(PATH_OUTPUT + "\log.txt", "a") as log:
        now = datetime.now()
        now = now.strftime(f"[%Hh:%Mm:%Ss] : ")
        for _ in range(len(data)):
            log.write(f"{now}{data[_]}\n")

# Don't clutter the working directory, make a temporary one
try:
    os.mkdir(PATH_OUTPUT)
except FileExistsError:
    pass
finally:
    os.mkdir(PATH_TEMP)

urls = {
    "iPhone 13 Pro Max 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-256gb-alpine-green-a-pouzity-p-140126",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-256gb-alpine-green-pouzite-p-140127",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-256gb-alpine-green-c-pouzity-p-140128"
    },
    "iPhone 13 Pro Max 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-128gb-alpine-green-a-pouzity-p-140119",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-128gb-alpine-green-pouzite-p-140120",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-max-128gb-alpine-green-c-pouzity-p-140121"
    },
    "iPhone 13 Pro 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-256gb-silver-a-pouzity-p-129175",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-256gb-silver-pouzite-p-129176",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-256gb-silver-c-pouzity-p-129177"
    },
    "iPhone 13 Pro 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-128gb-alpine-green-a-pouzity-p-140287",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-128gb-alpine-green-pouzite-p-140288",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-pro-128gb-alpine-green-c-pouzity-p-140289"
    },
    "iPhone 13 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-256gb-midnight-a-pouzity-p-129294",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-256gb-midnight-pouzite-p-129295",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-256gb-midnight-c-pouzity-p-129296"
    },
    "iPhone 13 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-128gb-green-a-pouzity-p-140315",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-128gb-green-pouzite-p-140316",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-128gb-green-c-pouzity-p-140317"
    },
    "iPhone 13 Mini 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-mini-256gb-green-a-pouzity-p-140343",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-mini-256gb-green-pouzite-p-140344",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-mini-256gb-green-c-pouzity-p-140345"
    },
    "iPhone 13 Mini 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-mini-128gb-midnight-a-pouzity-p-129376",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-mini-128gb-midnight-pouzite-p-129377",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-13-mini-128gb-midnight-c-pouzity-p-129378"
    },
    "iPhone 12 Pro Max 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-pro-max-128gb-graphite-a-pouzity-p-117173",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-pro-max-128gb-graphite-pouzite-p-117174",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-pro-max-128gb-graphite-c-pouzity-p-117175"
    },
    "iPhone 12 Pro 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-pro-128gb-pacific-blue-a-pouzity-p-117064",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-pro-128gb-pacific-blue-pouzite-p-117065",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-pro-128gb-pacific-blue-c-pouzity-p-117066"
    },
    "iPhone 12 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-128gb-white-a-pouzity-p-116920",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-128gb-white-pouzite-p-116921",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-128gb-white-c-pouzity-p-116922"
    },
    "iPhone 12 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-64gb-white-a-pouzity-p-116860",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-64gb-white-pouzite-p-116861",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-64gb-white-c-pouzity-p-116862"
    },
    "iPhone 12 Mini 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-mini-128gb-blue-a-pouzity-p-116764",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-mini-128gb-blue-pouzite-p-116765",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-mini-128gb-blue-c-pouzity-p-116766"
    },
    "iPhone 12 Mini 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-mini-64gb-black-a-pouzity-p-116668",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-mini-64gb-black-pouzite-p-116669",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-12-mini-64gb-black-c-pouzity-p-116670"
    },
    "iPhone 11 Pro Max 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-max-256gb-gold-a-pouzity-p-104068",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-max-256gb-gold-pouzite-p-104069",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-max-256gb-gold-c-pouzity-p-104070"
    },
    "iPhone 11 Pro Max 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-max-64gb-midnight-green-a-pouzity-p-104032",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-max-64gb-midnight-green-pouzite-p-104033",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-max-64gb-midnight-green-c-pouzity-p-104034"
    },
    "iPhone 11 Pro 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-256gb-space-gray-a-pouzity-p-103896",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-256gb-space-gray-pouzite-p-103897",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-256gb-space-gray-c-pouzity-p-103898"
    },
    "iPhone 11 Pro 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-64gb-midnight-green-a-pouzity-p-103884",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-64gb-midnight-green-pouzite-p-103885",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-pro-64gb-midnight-green-c-pouzity-p-103886"
    },
    "iPhone 11 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-128gb-black-a-pouzity-p-103704",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-128gb-black-pouzite-p-103705",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-128gb-black-c-pouzity-p-103706"
    },
    "iPhone 11 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-64gb-green-a-pouzity-p-103680",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-64gb-green-pouzite-p-103681",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-11-64gb-green-c-pouzity-p-103682" 
    },
    "iPhone Xs 256 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xs-256gbsilver-pouzity-kata-p-92288",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xs-256gb-silver-pouzite-p-92289",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xs-256gb-silver-pouzite-katc-p-92290"
    },
    "iPhone Xs 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xs-64gbsilver-pouzity-kata-p-92252",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xs-64gb-silver-pouzite-p-92253",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xs-64gb-silver-pouzite-katc-p-92254"
    },
    "iPhone Xr 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xr-128gbblack-pouzity-kata-p-92087",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xr-128gb-black-pouzite-p-92088",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xr-128gb-black-c-pouzity-p-92089"
    },
    "iPhone Xr 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xr-64gbblack-pouzity-kata-p-92012",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xr-64gb-black-pouzite-p-92013",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-xr-64gb-black-c-pouzity-p-92014"
    },
    "iPhone X 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-x-64gbspace-gray-pouzity-kata-p-54896",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-x-64gb-space-gray-pouzity-p-43493",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-x-64gb-space-gray-c-pouzity-p-51840"
    },
    "iPhone SE 2022 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-5g-2022-128gb-productred-a-pouzity-p-140449",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-5g-2022-128gb-productred-pouzite-p-140450",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-5g-2022-128gb-productred-c-pouzity-p-140451"
    },
    "iPhone SE 2022 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-5g-2022-64gb-midnight-a-pouzity-p-140421",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-5g-2022-64gb-midnight-pouzite-p-140422",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-5g-2022-64gb-midnight-c-pouzity-p-140423"
    },
    "iPhone SE 2020 128 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-2020-128gb-white-a-pouzity-p-110391",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-2020-128gb-white-pouzite-p-110392",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-2020-128gb-white-c-pouzity-p-110393"
    },
    "iPhone SE 2020 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-2020-64gb-black-a-pouzity-p-110343",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-2020-64gb-black-pouzite-p-110344",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-se-2020-64gb-black-c-pouzity-p-110345"
    },
    "iPhone 8 64 GB" : {
        "A" : "https://www.mp.cz/mobilni-telefon-apple-iphone-8-64gbsilver-pouzity-kata-p-54880",
        "B" : "https://www.mp.cz/mobilni-telefon-apple-iphone-8-64gb-silver-pouzity-p-37457",
        "C" : "https://www.mp.cz/mobilni-telefon-apple-iphone-8-64gb-silver-c-pouzity-p-51824"
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

abc, entries = [], []
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
                name = NOW.strftime("%f")
                _name = name
            else:
                DRIVER.get(v2)
                entries.append(name)
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
            logger(f"{times} Files Acquired")
            
    return times

times = downloader()

def redownloader():
    broken = entries.index(_)
    retry = links[broken]
    logger(f"Link: {retry}")
    _name = downloader(retry=retry)
    _name = PATH_TEMP_NEW + _name + ".mhtml"
    with open(_name, "r") as retried:
        _data = retried.read()
        _found = findall(P2, _data)
        if len(_found) == 0:
            _found = findall(P1, _data)
        if len(_found) > 1:
            result = f"Error: {_found} | Might require manual check"
            result = result.replace("&nbsp;", " ")
            result = result.replace("K=C4=8D", "")
        else:
            result = _found[0]
            result = result.replace("&nbsp;", " ", 1)
            result = result.replace("&nbsp;K=C4=8D", "")
    
    return result

def finder(temp_name, file_name):
    try:
        with open(temp_name, "r") as temp:
            data = temp.read()
            found = findall(P2, data)
            if len(found) == 0:
                found = findall(P1, data)
            if len(found) > 1:
                # given it's very unlikely to occur, it should probably be looked at
                result = f"Error: {found} | Might require manual check"
                result = result.replace("&nbsp;", " ")
                result = result.replace("K=C4=8D", "")
            elif len(found) == 0:
                logger(f"File Not Found: {file_name}")
                result = redownloader()
            elif len(found) == 1:
                result = found[0]
                result = result.replace("&nbsp;", " ", 1)
                result = result.replace("&nbsp;K=C4=8D", "")
    except FileNotFoundError:
        logger(f"File Not Found: {file_name}")
        result = redownloader()
    
    return result

logger(entries)
logger(f"Download Of {times} Files Complete")

#input("Debug Pause ")

headers = list(urls.keys())
done, header = 0, 0
while True:
    if times != PHONES:
        sleep(5) # Preserve resources by delaying another iteration
        logger("Delaying The Script...")
    else:
        logger("Analyzing...")
        sleep(3) # Make sure the code below isn't run before last file is saved
        with open(PATH_OUTPUT + "\Prices.txt", "w") as cost:
            cost.write(f"{headers[done]}:\n")
            header += 1
            for _ in entries:
                file_name = f"'{_}.mhtml'"
                temp_name = PATH_TEMP_NEW + _ + ".mhtml"
                result = finder(temp_name, file_name)
                if abc[done] == "C":
                    cost.write(f"    {abc[done]} : {result}\n\n")
                    try:
                        cost.write(f"{headers[header]}:\n")
                        header += 1
                    except IndexError:
                        pass
                else:
                    cost.write(f"    {abc[done]} : {result}\n")
                done += 1
        if done == PHONES:
            logger("Removing Temp Files...")
            rmtree(PATH_TEMP) # Remove our temporary files to free up space
            break

logger(f"Operation Successful, Output Located In {PATH_OUTPUT}")
