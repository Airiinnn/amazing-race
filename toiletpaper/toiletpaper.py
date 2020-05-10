import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
rolls = 1
total = rolls

for i in range(28):
    rolls *= 2
    total += rolls
    
print(int(total * 5.2))