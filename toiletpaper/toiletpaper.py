import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
c = 1
s = 0
for i in range(29):
    s += c*2
    c*=2
s *=5.2
print(int(s))