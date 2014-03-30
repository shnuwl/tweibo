# coding:utf-8
u =u'\u671f👌\u671f'
s = repr(u)
print s
q = s.replace('U','0')
print s
print type(unicode(q))
a = unicode(q)
b = a.encode('utf-8')
print a