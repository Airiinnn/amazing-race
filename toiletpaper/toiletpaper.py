import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
s=0
c=1
for i in range(29):
    s+=c
    c*=2
print(int(s*5.2))
