#encoding=utf-8
import os
import sys
import time
import uuid
import web

from db_info import db_tpms

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class MysqlControl:
    def __init__(self):
        self.db = db_tpms

    # 分析用户的text，去掉"||"和"@"后的多余内容
    def cut_string(self, text):
        i = text.find("||")
        j = text.find("@")
        if (i != -1) and (j != -1):
            return min(i,j)
        elif (i == -1) and (j == -1):
            return len(text)
        else:
            return max(i, j)

    # 各种数据库查询和插入方法
    # 插入用户个人信息入数据库
    def insert_user_info(self, x):
        userList = list(self.db.select('t_user', what="name", where="uid=\""+x.name+"\""))
        if not userList:
            info = self.db.insert('t_user', uid=x.name, name=x.nick, sex=x.sex, introduction=x.introduction,
                                  isvip=x.isvip, verifyinfo=x.verifyinfo, location=x.location, fansnum= x.fansnum,
                                  favnum=x.favnum, idolnum=x.idolnum, mutual_fans_num=x.mutual_fans_num,
                                  regtime=x.regtime, tweetnum=x.tweetnum)
            if info == 0:
                curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print "Added %s's info successful! %s" % (x.name, curTime)

    # 插入中心用户和双向收听用户之间映射关系入数据库
    def insert_f_relation(self, mutual_name, name_list):
        where_dict = {"centeruid":mutual_name, "sourceuid":mutual_name}
        userList = list(self.db.select('t_relations', what="targetuid", where=web.db.sqlwhere(where_dict)))
        num = 0
        if not userList:
            for tname in name_list:
                uid = str(uuid.uuid1())[:8]+str(uuid.uuid1())[19:23]
                info =self.db.insert("t_relations", id=uid, centeruid=mutual_name, sourceuid=mutual_name,
                                     targetuid=tname, deep=1)
                num += (1-info)
        curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print "Added %d new f_records to 't_relations' %s" % (num,curTime)

    # 双向收听用户之间又会有双向收听的，把此关系插入数据库
    def insert_s_relation(self, mutual_name, s_name, name_list):
        where_dict = {"centeruid":mutual_name, "sourceuid":s_name}
        userList = list(self.db.select('t_relations', what="targetuid", where=web.db.sqlwhere(where_dict)))
        num = 0
        if not userList:
            for tname in name_list:
                uid = str(uuid.uuid1())[:8]+str(uuid.uuid1())[19:23]
                info =self.db.insert("t_relations", id=uid, centeruid=mutual_name, sourceuid=s_name,
                                     targetuid=tname, deep=2)
                num += (1-info)
        curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print "Added %d new s_records to 't_relations' %s" % (num, curTime)
        
    # 插入转发列表入数据库
    def insert_r_list(self, x, r_list, uid=None):
        # 导入分词模块，用于计算每个微博文本中褒义词和贬义词的个数
        from smallseg.fenci import fenci
        f = fenci()
        num = 0
        for _list in r_list:
            if _list.text:
                userList = list(self.db.select('t_texts', what="name", where="id=\""+_list.id+"\""))
                if not userList:
                    n = self.cut_string(_list.text)
                    _text = _list.text[:n]
                    Text = repr(_text)
                    # 表情符号由'/Uxxxxxxxx'来表示，目前存入数据库会出错，所以筛选之
                    if Text.find('U') != -1:
                        continue
                    atti = f.deal_text(_text)
                    try:
                        info = self.db.insert('t_texts', id=_list.id, sourceid=x, uid=_list.name, name=_list.nick,
                                              text=_text, isvip=_list.isvip, attitude=atti)
                    except Exception, ex:
                        print "Database Input Exception %s" % ex
                    else:
                        num += (1 - info)
        if x == 100:#根用户的微博文本信息被存入
            curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print "%s:Added %d new records to 't_texts' %s" % (uid, num, curTime)
        else:#转发者的微博文本信息被存入
            curTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print "Added %d new records to 't_texts' %s" % (num, curTime)

