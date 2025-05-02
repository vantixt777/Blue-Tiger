@echo off
echo Installiere alle benötigten Python-Module...

REM Sicherstellen, dass pip funktioniert
python -m ensurepip --upgrade
python -m pip install --upgrade pip

REM Python-Module über pip installieren
pip install requests
pip install beautifulsoup4
pip install phonenumbers
pip install dnspython
pip install whois
pip install opencv-python
pip install numpy
pip install scapy
pip install exifread
pip install aiohttp
pip install pillow
pip install colorama
pip install termcolor
pip install webbrowser
pip install selenium
pip install pytesseract
pip install python-whois
pip install social-analyzer
pip install metadata-parser
pip install geocoder
pip install ipwhois
pip install pyfiglet
pip install folium
pip install google
pip install youtube-dl
pip install instaloader
pip install twint
pip install praw
pip install pygments
pip install tqdm
pip install psutil
pip install networkx
pip install matplotlib
pip install pandas
pip install imagehash
pip install face_recognition
pip install pyexiftool
pip install telegram
pip install termcolor
pip install discord.py
pip install pywhatkit
pip install shodan

REM Optional: falls Pillow mehrfach erwähnt wurde
pip install --upgrade pillow

REM Optional: Installiere wichtige Tools
pip install --upgrade git+https://github.com/sherlock-project/sherlock.git
pip install --upgrade git+https://github.com/Datalux/Osintgram.git

echo.
echo Alle Module wurden (sofern möglich) installiert.
pause