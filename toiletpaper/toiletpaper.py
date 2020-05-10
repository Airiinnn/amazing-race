import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
<<<<<<< HEAD
rolls = 1
total = rolls

for i in range(28):
    rolls *= 2
    total += rolls
    
print(int(total * 5.2))
=======
s=0

c=1

for i in range(29):

    s+=c

    c*=2

print(int(s*5.2))
>>>>>>> 00cd6a24a369cc769f3813d1aadcf643437741f1
