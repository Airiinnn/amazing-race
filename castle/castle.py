import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
for i in range(3):
    a = int(input())
    b = int(input())
    
    print(a*b)