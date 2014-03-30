#encoding=utf-8
import os
_localDir=os.path.dirname(__file__)
_curpath=os.path.normpath(os.path.join(os.getcwd(),_localDir))
curpath=_curpath
p_list=[x.rstrip().decode('utf-8') for x in file(os.path.join(curpath,"positive.dic")) ]
n_list=[x.rstrip().decode('utf-8') for x in file(os.path.join(curpath,"negative.dic")) ]
from smallseg import SEG
seg = SEG()

class fenci:
    def deal_text(self,text):
        p = 0
        n = 0
        wlist = seg.cut(text)
        for i in wlist:
            if i in p_list:
                p+=1
            if i in n_list:
                n+=1
        # 褒义词个数多于贬义词的个数，态度设为1，少于则设为-1，否则设为0
        if p > n:
            return 1
        elif p == n:
            return 0
        else:
            return -1