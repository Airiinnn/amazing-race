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
    N, M = input().strip().split()
    N = int(N)
    M = int(M)

    print(fib(N, M))

    
    
    
    
    
    
    
    
    
    