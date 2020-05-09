import sys
sys.modules['os']=None
sys.modules['sqlite3']=None
sys.modules['flask']=None
sys.modules['subprocess']=None
sys.modules['sys']=None
del sys
def fib(n, m):
    f = [0, 1]
    
    for i in range(2, n+1):
        f.append((f[i-1] + f[i-2]) % m)
        
    return f[n]

T = int(input())

for _ in range(T):
    temp = input().strip().split()
    N = int(temp[0].strip())
    M = int(temp[1].strip())
    
    print(fib(N, M))