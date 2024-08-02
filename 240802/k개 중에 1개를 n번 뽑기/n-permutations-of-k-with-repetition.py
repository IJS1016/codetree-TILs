K, N = map(int, input().split())

def choose(l) :
    if len(l) == N:
        print(" ".join(map(str, l)))
        return
    for i in range(1, K+1) :
        choose(l + [i])

choose([])