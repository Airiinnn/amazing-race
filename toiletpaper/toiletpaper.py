import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
rolls=1
total=0

for i in range(29):
    total += rolls
    rolls *= 2

print(int(total * 5.2))
