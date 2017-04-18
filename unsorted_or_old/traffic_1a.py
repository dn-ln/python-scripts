#! /usr/bin/env python3
import time, paramiko, os
starttime = time.time()
usr = os.environ['CAMUSERID']
pwd = os.environ['CAMPASSWORD']
client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect('192.168.2.222', username = usr, password = pwd)

while True:
  counttime = time.time()
  if counttime - starttime >= 60:
    stdin, stdout, stderr = client.exec_command('PATH=$PATH:/usr/sbin; restart_command')
    starttime += 60
