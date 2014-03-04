#encoding=utf-8
import os, sys, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from db_info import db_tpms
from mydb import MysqlControl

class RelistControl:

    def get_relist(self,id,Api):
        # GET /t/re_list
        i = 0
        sw = 0
        pt = 0
        tid = 0
        r_list = list()
        # 本来是想抓取所有的转播信息，但是动辄几千条，太浪费时间，改为了只抓取500条
        while i == 0:
            t_relist = Api.get.t__re_list(format="json", flag=2, rootid=id, pageflag=1,pagetime=pt, reqnum=100, twitterid=tid)
            time.sleep(3.6)
            if t_relist.data == None:
                print id+" no relay list!"
                break
            r_list.extend(t_relist.data.info)
            sw += 1
            if sw == 5:
                break
            i = t_relist.data.hasnext
            if i == 0:
                pt = t_relist.data.info[-1]["timestamp"]
                tid = t_relist.data.info[-1]["id"]
        if r_list != []:
            msc = MysqlControl()
            msc.insert_r_list(id,r_list)