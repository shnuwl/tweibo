import web,os
from configobj import ConfigObj

conf = ConfigObj(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.ini'))
db_info = conf['DB']
db_tpms = web.database(dbn='mysql', db = 'weibo', user = db_info['USER'], pw= db_info['PASS'], host = db_info['HOST'])
db_tpms.printing = False