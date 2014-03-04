import web,os,time
from configobj import ConfigObj

conf = ConfigObj(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.ini'))
db_info = conf['NAME']
user = db_info['names']
print type(user)
while True:
    for i in user:
        print i
        print type(i)
        time.sleep(1)