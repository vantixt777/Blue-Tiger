@echo off
echo Installiere alle benötigten Python-Module...

REM Sicherstellen, dass pip funktioniert
python -m ensurepip --upgrade

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

REM Optional: falls Pillow mehrfach erwähnt wurde
pip install --upgrade pillow

REM Hinweis: Standard-Module wie os, sys, time, json, re usw. müssen NICHT installiert werden

echo.
echo Alle Module wurden (sofern möglich) installiert.
pause
