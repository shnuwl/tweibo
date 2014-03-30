#encoding=utf-8
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from db_info import db_tpms
from mydb import MysqlControl

class MutualControl:
    def get_relations(self, n_list, Api):
        _dict = {}
        for name in n_list:
            List = self.get_mutual(name, Api)
            if List:
                s_list = list()
                for s_name in List:
                    if (s_name in n_list) and (s_name not in _dict):
                        s_list.append(s_name)
                if s_list:
                    _dict[name] = s_list
        return _dict
        
    def insert_mutuals(self, mutual_name, Api):
        mysqlContol = MysqlControl()
        user_info = Api.get.user__other_info(format="json", name=mutual_name)
        mysqlContol.insert_user_info(user_info.data)
        time.sleep(3.6)
        n_list = self.get_mutual(mutual_name, Api)
        if n_list:
            mysqlContol.insert_f_relation(mutual_name, n_list)
            for name in n_list:
                user_info = Api.get.user__other_info(format="json", name=name)
                mysqlContol.insert_user_info(user_info.data)
                time.sleep(3.6)
            d_relation = self.get_relations(n_list, Api)
            if d_relation:
                for x in d_relation.keys():
                    y = d_relation[x]
                    mysqlContol.insert_s_relation(mutual_name, x, y)
            curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print "Completed the tasks of input %s's mutual info! %s" % (mutual_name, curTime)

    def get_mutual(self, mutual_name, Api):
        # GET /friends/mutual_list
        i = 0
        s_index = 0
        name_list = list()
        while not i:
            t_mutual = Api.get.friends__mutual_list(format="json", name=mutual_name, startindex=s_index, reqnum=30)
            curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print "acquired %s's mutual list! %s" % (mutual_name, curTime)
            time.sleep(3.6)
            if t_mutual.data is None:
                curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print "%s has no mutual friends! %s" % (mutual_name, curTime)
                break
            else:
                name_list.extend([x.name for x in t_mutual.data.info])
                i = t_mutual.data.hasnext
                s_index += 30
        return name_list