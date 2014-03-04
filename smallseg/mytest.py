import os
_localDir=os.path.dirname(__file__)
_curpath=os.path.normpath(os.path.join(os.getcwd(),_localDir))
curpath=_curpath
print([x.rstrip() for x in file(os.path.join(curpath,"suffix.dic")) ])