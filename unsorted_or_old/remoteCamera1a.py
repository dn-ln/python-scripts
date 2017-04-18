#! /usr/bin/env python3
import paramiko, socket, os, sys
try:
  ip = sys.argv[1]

  usr = os.environ['CAMUSERID']
  pwd = os.environ['CAMPASSWORD']
  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()
  ssh.connect(ip, username = usr, password = pwd)

  while True:
    cmd = input('xxx@<ip>: ')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.readlines()
    print(type(stdout))
    print(lines)
    for line in lines:
      print(line.rstrip('\n'))

except IndexError:  
  print('./remoteCamera.py <ip address>')

except socket.error:
  print('The IP might be wrong. Try again.')
  
