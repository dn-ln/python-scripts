#! /usr/bin/env python3.5
from datetime import datetime, timedelta
from random import randint, choice
import sys, re, os, subprocess


env = {"email": os.environ['UMBOUSER'], "password": os.environ['UMBOPWD']}
env_str = str(env).replace("'", '"')
cmd = '''curl -X POST -d '{}' -H "Content-Type: application/json" url'''.format(env_str)

output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True)
output2 = output.decode('ascii')
pattern = re.compile(r'"token":"(.+?)"')
token = pattern.search(output2).group(1)

days = int(sys.argv[1])
d0 = datetime.today()

jumboId = "ID-1C21D1C0096F" 						     # Camera JumboId
count = 0

while days >= count:

  ''' For CV Alert
  rhour, rmin, rsec = randint(0, 23), randint(0, 59), randint(0, 59) # rmicro = randint(0, 999999) => If you want to generate random microseconds   
  roiId = "Zone " + str(randint(1, 3))				     
								     # jumboId = "ID-1C21D1C0" + ''.join([choice(hexchoice) for i in range(4)]) => Random jumboId
  t = timedelta(days=count)
  d1 = d0 - t
  d2 = d1.replace(hour=rhour, minute=rmin, second=rsec, microsecond=0)
  d3 = d2.timestamp()						     # UNIX timestamp * 1000 => MongoDB ISODate
  d4 = d2.strftime('%Y-%m-%d:%H:%M:%S') 			     # d5 = d2.isoformat() => if you want to have isoformat

  
  data = {"jumboId": jumboId, "roiId": roiId, "snapshot": "https://www.xxx.com/images/page_learnc_01-2.07877134.png", "previewVideo": "https://www.xxx.com/images/page_learnc_01-2.07877134.png", "beginTime": int(d3) * 1000, "objectType": "person"}
  '''

  codeopt = [('Disconnect', '0x81000002'), ('Overheat', '0x81000003'), ('Fail Record', '0x80070002'), ('Fail Record', '0x800A0002'), ('Fail Record', '0x800A0003')]
  ropt = randint(0, 4)
  data = {"jumboId": jumboId, "umbo_code": codeopt[ropt][1], "message": codeopt[ropt][0]}
  d4 = d0.isoformat()


  data2 = str(data).replace("'", '"')
  data_str = "curl -i -X POST -d '{}'".format(data2)

  h1 = '-H "Authorization: Bearer {}"'.format(token)
  h2 = '-H "Content-Type: application/json"'
  h3 = '-H "Accept: application/json"'
  # url = 'url' 	     # => for CV alert		     
  url = 'url' 		     # => for alert
  l = [data_str, h1, h2, h3, url]

  cmd2 = ' '.join(l)
  subprocess.run(cmd2, shell=True)

  with open('mylog.txt', 'a') as f:
    f.write(cmd2 + ' #' + d4 + '\n\n')
      
  count += 1

with open('mylog.txt', 'a') as f:
  f.write('<================End of Ouput=================>' + '\n\n')
