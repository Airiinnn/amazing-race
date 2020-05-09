import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
T = int(input())

for _ in range(T):
    cost = 0
    n = int(input())
    start = input().strip().split()
    increase = input().strip().split()
    
    for i in range(n):
        start[i] = int(start[i].strip())
        increase[i] = int(increase[i].strip())
    
    increase.sort()
    
    for i in range(n):
        cost += increase[i] * (n-i-1) + start[i]
        
    print(cost)
