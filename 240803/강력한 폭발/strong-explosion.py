import copy
bombs = [[[-2, 0], [-1, 0], [1, 0], [2, 0]], 
         [[-1, 0], [0, -1], [1, 0], [0, 1]], 
         [[-1, -1], [-1, 1], [1, -1], [1, 1]]]

N = int(input())
mmap = [list(map(int, input().split())) for _ in range(N)]
max_v = 0

bomb_locations = []
for y, m in enumerate(mmap) :
    for x, v in enumerate(m) :
        if mmap[y][x] :
            bomb_locations.append([y, x])
            mmap[y][x] = 8

N_bl = len(bomb_locations)
def print_mmap(mmap) :
    for m in mmap :
        print(" ".join(map(str, m)))

def is_in_range(y, x) :
    return 0 <= y < N and 0 <= x < N

def put_bombs(mmap, bomb, y, x, bi) :
    mmap[y][x] = bi+2
    for dy, dx in bomb :
        if is_in_range(y+dy, x+dx) :
            mmap[y+dy][x+dx] = 1
    # print_mmap(mmap)
    return mmap

def count_baam(mmap) :
    result = 0
    for y, m in enumerate(mmap) :
        for x, v in enumerate(m) :
            if mmap[y][x] :
                result += 1
    return result

def check_bombs(mmap, bomb_locations) :
    global max_v
    if not len(bomb_locations) :
        tmp_v = count_baam(mmap) 
        if max_v < tmp_v :
            max_v = tmp_v
        return

    # 폭탄 놓을 수 있는 위치에 폭탄 설치
    by, bx = bomb_locations[0]
    for bi, bomb in enumerate(bombs) :
        # print(f"put {bi+2} bomb {by}, {bx}")
        check_bombs(put_bombs(copy.deepcopy(mmap), bomb, by, bx, bi), bomb_locations[1:])

check_bombs(mmap, bomb_locations)
print(max_v)

# 새로운 mmap을 생성해서, 넣어주고
# 폭탄 들어가는 자리는 -1로 설정
# 폭탄 1, 2, 3으로 두고 -> 표시할 필요가 없지... 그냥 1로 두면 됨
# 초토화는 bombs 새로운거로 표시하면서 다 더해주기
# visited로 폭탄 설치 표시 => 위치를 리스트로 저장