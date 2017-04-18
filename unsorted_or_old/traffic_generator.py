#! /usr/bin/env python3
import paramiko, os, re, time, threading
from datetime import datetime

usr = os.environ['CAMUSERID']
pwd = os.environ['CAMPASSWORD']
p = re.compile(r'(2016.+?)\s(.+?)\s(.+?)\n')

class cameraThread(threading.Thread):
  def __init__(self, name, trafficfile):
    threading.Thread.__init__(self)
    self.name = name 
    with open(trafficfile) as f:
      f_r = f.read()
      self.trafficlines = p.findall(f_r)
      self.ip = p.search(f_r).group(2)
  def run(self):
    print(self.name + ' Connecting')
    traffic(self.name, self.ip, self.trafficlines)
    print(self.name + ' Exiting')

lock = threading.Lock()

def traffic(name, ip, tlines):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  lock.acquire()
  client.connect(ip, username = usr, password = pwd)
  lock.release()
  for line in tlines:
    t = line[0]
    cmd = line[2]
    t1 = datetime.strptime(t, '%Y.%m.%dT%H:%M:%S').timestamp()  
    t0 = datetime.now().timestamp()
    if t1 - t0 >= 0:
      time.sleep(t1 - t0)
      stdin, stdout, stderr = client.exec_command('PATH=$PATH:/usr/sbin; ' + cmd)
      print(name + '(%s): ' % ip + cmd + ' ' + datetime.now().isoformat())
    else:
      pass
  client.close()

camera1, camera2, camera3 = cameraThread('cam1', 'traffic1.txt'), cameraThread('cam2', 'traffic2.txt'), cameraThread('cam3', 'traffic3.txt')


cameras = [camera1, camera2, camera3]

for camera in cameras:
  camera.start()

for camera in cameras:
  camera.join()

print('All Traffics Finished')






  
