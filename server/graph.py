#encoding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from db_info import db_tpms

class GraphControl:
    def select_gdata(self, info):
        # 从"t_texts"和"t_relations"里读取数据，组成JSON
        i = 0
        _dic = {}
        links = list()
        nodes = list()
        childLinks = list()
        childNodes = list()
        uid = info.uid
        textList = list(db_tpms.select('t_texts', what="id, name, text, attitude", where="uid=\""+uid+"\"", limit=1))
        id = textList[0].id
        textList1 = list(db_tpms.select('t_texts', what="name, text, attitude", where="sourceid=\""+id+"\"", limit=50))
        for t in textList1:
            if t.text:
                childLinks.append({'source':textList[0].name, 'target':t.name, 'value':'3'})
                childNodes.append({'id':t.name, 'text':t.text, 'attitude':t.attitude})
        userList = list(db_tpms.select('t_relations', what="sourceuid, targetuid, deep", where="centeruid=\""+uid+"\""))
        for x in userList:
            if x.sourceuid not in _dic.values():
                _dic[i] = x.sourceuid
                i+=1
            if x.targetuid not in _dic.values():
                _dic[i] = x.targetuid
                i += 1
        for y in userList:
            s = y.sourceuid
            t = y.targetuid
            links.append({'source':self.get_name(s), 'target':self.get_name(t), 'value':y.deep})
        for u in _dic.values():
            k = 0
            for y in userList:
                if u == uid:
                    name = self.get_name(u)
                    nodes.append({'count':15, 'id':name, 'text':textList[0].text, 'attitude':textList[0].attitude,
                                 'expand':True})
                    break
                if u in [y.sourceuid, y.targetuid]:
                    k += 1
            if k:
                name = self.get_name(u)
                nodes.append({'count':k, 'id':name})
        return {'links':links, 'nodes':nodes, 'childLinks':childLinks, 'childNodes':childNodes}
        
    #获取用户的昵称
    def get_name(self, uid):
        Name = list(db_tpms.select('t_user', what="name", where="uid=\""+uid+"\""))[0]
        return Name.name