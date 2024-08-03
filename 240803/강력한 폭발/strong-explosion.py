# # 새로운 mmap을 생성해서, 넣어주고
# # 폭탄 들어가는 자리는 -1로 설정
# # 폭탄 1, 2, 3으로 두고 -> 표시할 필요가 없지... 그냥 1로 두면 됨
# # 초토화는 bombs 새로운거로 표시하면서 다 더해주기
# # visited로 폭탄 설치 표시 => 위치를 리스트로 저장

# # copy 사용
# import copy
# bombs = [[[-2, 0], [-1, 0], [1, 0], [2, 0]], 
#          [[-1, 0], [0, -1], [1, 0], [0, 1]], 
#          [[-1, -1], [-1, 1], [1, -1], [1, 1]]]

# N = int(input())
# mmap = [list(map(int, input().split())) for _ in range(N)]
# max_v = 0

# bomb_locations = []
# for y, m in enumerate(mmap) :
#     for x, v in enumerate(m) :
#         if mmap[y][x] :
#             bomb_locations.append([y, x])
#             mmap[y][x] = 8

# N_bl = len(bomb_locations)
# def print_mmap(mmap) :
#     for m in mmap :
#         print(" ".join(map(str, m)))

# def is_in_range(y, x) :
#     return 0 <= y < N and 0 <= x < N

# def put_bombs(mmap, bomb, y, x, bi) :
#     mmap[y][x] = bi+2
#     for dy, dx in bomb :
#         if is_in_range(y+dy, x+dx) :
#             mmap[y+dy][x+dx] = 1
#     # print_mmap(mmap)
#     return mmap

# def count_baam(mmap) :
#     result = 0
#     for y, m in enumerate(mmap) :
#         for x, v in enumerate(m) :
#             if mmap[y][x] :
#                 result += 1
#     return result

# def check_bombs(mmap, bomb_locations) :
#     global max_v
#     if not len(bomb_locations) :
#         tmp_v = count_baam(mmap) 
#         if max_v < tmp_v :
#             max_v = tmp_v
#         return

#     # 폭탄 놓을 수 있는 위치에 폭탄 설치
#     by, bx = bomb_locations[0]
#     for bi, bomb in enumerate(bombs) :
#         # print(f"put {bi+2} bomb {by}, {bx}")
#         check_bombs(put_bombs(copy.deepcopy(mmap), bomb, by, bx, bi), bomb_locations[1:])

# check_bombs(mmap, bomb_locations)
# print(max_v)

# # copy 사용 안하고 하는 방법 없을까?
# # 폭탄 터진 위치를 list로 저장? 위치도 deepcopy 해줘야됨

# # 해설 공부
# # 폭탄 위치, 종류에 대한 모든 경우의 순열을 만들면 deepcopy 필요 없지
# # 0으로 가득 찬 list를 copy해서... 넘겨주면 걔가 알아서 돌도록하면 적어도 폭탄 설치할 떄마다는 copy 안해도 되지
# # 정답에서는 bombed를 초기화해줘서 copy 안하도록 하네
# # 전체 위치 돌면서... 아닌데 bomb_pos 정의해줬는대..?

# # if로 안하고 max(x, y) 이런식으로 하면 더 깔꼼

# # bomb type으로 폭탄을 먼저 배치한뒤에, 초기화 된 bomb에 터트린 후, 전체 초토화 된 영역 수 구함
# # 비슷한데..?

# 변수 선언 및 입력:
n = int(input())
bomb_type = [
    [0 for _ in range(n)]
    for _ in range(n)
]
bombed = [
    [False for _ in range(n)]
    for _ in range(n)
]

ans = 0

bomb_pos = list()


def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


def bomb(x, y, b_type):
    # 폭탄 종류마다 터질 위치를 미리 정의합니다.
    bomb_shapes = [
        [],
        [[-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0]],
        [[-1, 0], [1, 0], [0, 0], [0, -1], [0, 1]],
        [[-1, -1], [-1, 1], [0, 0], [1, -1], [1, 1]]
    ]
    
    # 격자 내 칸에 대해서만 영역을 표시합니다.
    for i in range(5):
        dx, dy = bomb_shapes[b_type][i];
        nx, ny = x + dx, y + dy
        if in_range(nx, ny):
            bombed[nx][ny] = True

            
def calc():
    # Step1. 폭탄이 터진 위치를 표시하는 배열을
    # 초기화합니다.
    for i in range(n):
        for j in range(n):
            bombed[i][j] = False
            
    # Step2. 각 폭탄의 타입에 따라 
    # 초토화 되는 영역을 표시합니다.
    for i in range(n):
        for j in range(n):
            if bomb_type[i][j]:
                bomb(i, j, bomb_type[i][j])
	
    # Step3. 초토화된 영역의 수를 구합니다.
    cnt = 0
    for i in range(n):
        for j in range(n):
            if bombed[i][j]:
                cnt += 1
    
    return cnt


def find_max_area(cnt):
    global ans
    
    if cnt == len(bomb_pos):
        ans = max(ans, calc())
        return

    for i in range(1, 4):
        x, y = bomb_pos[cnt]
        
        bomb_type[x][y] = i
        find_max_area(cnt + 1)
        bomb_type[x][y] = 0


for i in range(n):
    given_row = list(map(int, input().split()))
    for j, bomb_place in enumerate(given_row):
        if bomb_place:
            bomb_pos.append((i, j))

find_max_area(0)

print(ans)