#encoding=utf-8
#! /usr/bin/env python
import os,sys
from configobj import ConfigObj
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from server.authorize import Authorize
from server.mutual import MutualControl
from server.relist import RelistControl
from server.usertimeline import TimelineControl

class Main:
    def __init__(self):
        self.api = Authorize().tweibo_authorize()
        print "Authorization success!"
    # 获取双向收听列表 
    def mutual_list(self,mutual_name):
        MutualControl().insert_mutuals(mutual_name,self.api)
    # 获取转发者信息
    def re_list(self,id):
        RelistControl().get_relist(id,self.api)
    # 获取一个人所发微博的列表
    def statuses_list(self,uid):
        # self.mutual_list(uid)
        w_list = TimelineControl().get_statuses(uid,self.api)
        for i in w_list:
            self.re_list(i.id)


if __name__ == '__main__':
    #Main().statuses_list("gxiaosong")
    main = Main()
    conf = ConfigObj(os.path.join(os.path.dirname(os.path.realpath(__file__)), './config.ini'))
    user_info = conf['old']
    user = user_info['names']
    while 1:
        for u in user:
            main.statuses_list(u)