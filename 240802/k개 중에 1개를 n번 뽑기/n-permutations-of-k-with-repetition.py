K, N = map(int, input().split())

def choose(n) :
    if len(n) == 2:
        print(" ".join(map(str, n)))
        return
    for i in range(1, K+1) :
        choose(n + [i])

choose([])