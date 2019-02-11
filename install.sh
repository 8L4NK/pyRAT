#!/bin/bash
# pyRAT v1.0
# Coded by @linux_choice (Don't change! Read the License!)
# Github: https://github.com/thelinuxchoice/pyRAT

command -v wine > /dev/null 2>&1 || { echo >&2 "I require wine but it's not installed. Installing..."; apt-get update && apt-get install wine; } 

printf "\e[1;93mDownloading Python2.7\e[0m\n"
wget https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi
printf "\e[1;93mInstalling Python2.7, you must continue the installation manually\e[0m\n"
wine msiexec /i python-2.7.15.msi /L*v log.txt
printf "\e[1;93mInstalling wine32\e[0m\n"
dpkg --add-architecture i386 && apt-get update && apt-get install wine32
cd ~/.wine/drive_c/Python27/
printf "\e[1;93mInstalling Python2.7 dependencies\e[0m\n"
wine python.exe Scripts/pip.exe install pyinstaller paramiko
printf "\e[1;92mDone!\e[0m\n"
