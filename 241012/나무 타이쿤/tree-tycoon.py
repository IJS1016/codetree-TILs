# 14:45 시작 두개 다 풀이?
# NxN 격자
# 다른 높이 리브로수

# 특수영양제
# 1x1 영역 리브로수 높이 1 증가, 씨앗일 경우 높이 1 리브로수
# 초기 NxN 격자 좌하단 4개 칸

# 이동
# 방향과 이동 칸 수가 정해짐
#  1 2 3 4 5 6 7 8 
#  → ↗ ↑ ↖ ← ↙ ↓ ↘
# 만약 범위가 넘으면 반대편으로 돌아옴(나머지처리하면 됨)

# 1년 동안
# 1. 특수 영양제 이동
# 2. 이동 후 영양제 투입(특수 영양제 사라짐)
# 3. 특수 영양제 투입 리브로수의 대각선으로 인접 방향 높이 1 이상인 리브로수 있는 만큼 높이가 더 성장, 격자 벗어나는 경우는 세지 않음
# 4. !! 특수 영양제 투입 X : 리브로수 높이가 2 이상 리브로수는 높이 2를 베어 잘라낸 리브로수로 특수 영양제 구매, 해당 위치에 특수 영양제 존재
# 14:45 시작 두개 다 풀이?
# import sys
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")

# INPUT ####################################################
#              →      ↗        ↑        ↖         ←         ↙       ↓        ↘
direction_names = ["→", "↗",  "↑",  "↖",  "←",  "↙",  "↓",  "↘"]
directions = [[0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]]
N, M = map(int, input().split())
tree_map = []
for _ in range(N) :
    tree_map.append(list(map(int, input().split())))

move_rules = []
for _ in range(M) :
    di, ms = list(map(int, input().split()))
    move_rules.append([di-1, ms])
nutri_list = [[N-1, 0], [N-1, 1], [N-2, 0], [N-2, 1]]
############################################################
# DEBUG ####################################################
def br() : return "\033[041m"
def bg() : return "\033[042m"
def by() : return "\033[043m"
def bb() : return "\033[000m"

def print_tree_map(tree_map, nutri_mmap) :
    for x in range(N):
        s = ""
        for y in range(N):
            if nutri_mmap[x][y] :
                s += bg()
            s += str(tree_map[x][y])
            s += bb()
            s += " "
        print(s)
############################################################
# FUNC  ####################################################
def check_in_range(x, y) :
    return 0 <= x < N and 0 <= y < N

def move_nutri(nutri_list, move_rule) :
    di, ms = move_rule
    tx, ty  = directions[di][0] * ms, directions[di][1] * ms

    new_nutri_list = []
    for (nx, ny) in nutri_list :
        new_nutri_list.append([(nx + tx + N) % N, (ny + ty + N) % N])

    return new_nutri_list

def set_nutri_map(nutri_list) :
    nutri_map = [[False for _ in range(N)] for _ in range(N)]
    for (nx, ny) in nutri_list:
        nutri_map[nx][ny] = True
    return nutri_map

def put_nutri(nutri_list, tree_map) :
    for (nx, ny) in nutri_list:
        tree_map[nx][ny] += 1

    for (nx, ny) in nutri_list:
        for di in [1, 3, 5, 7] :
            tx, ty = directions[di]
            if check_in_range(nx+tx, ny+ty) :
                if tree_map[nx+tx][ny+ty] >= 1 :
                    tree_map[nx][ny] += 1

    return tree_map

def buy_nutri(nutri_map, tree_map) :
    new_nutri_list = []
    for x in range(N) :
        for y in range(N) :
            if not nutri_map[x][y] :
                if tree_map[x][y] >= 2 :
                    tree_map[x][y] -= 2
                    new_nutri_list.append([x, y])
    return tree_map, new_nutri_list

def count_trees(tree_map) :
    result = 0
    for x in range(N) :
        for y in range(N) :
            result += tree_map[x][y]
    return result
############################################################
# MAIN  ####################################################
DBG = False
nutri_map = set_nutri_map(nutri_list)

for mi in range(M) :
    if DBG :
        print(f"\n>> ROUND {mi}")
        print("1. INIT")
        print_tree_map(tree_map, nutri_map)

    # 1. 특수 영양제 이동
    nutri_list = move_nutri(nutri_list, move_rules[mi])
    nutri_map = set_nutri_map(nutri_list)

    if DBG :
        print("2. MOVE NUTRI")
        print(direction_names[move_rules[mi][0]], move_rules[mi][1])
        print_tree_map(tree_map, nutri_map)

    # 2. 이동 후 영양제 투입(특수 영양제 사라짐)
    # 3. 특수 영양제 투입 리브로수의 대각선으로 인접 방향 높이 1 이상인 리브로수 있는 만큼 높이가 더 성장, 격자 벗어나는 경우는 세지 않음
    tree_map = put_nutri(nutri_list, tree_map)
    if DBG :
        print("3. PUT NUTRI NUTRI")
        print(direction_names[move_rules[mi][0]], move_rules[mi][1])
        print_tree_map(tree_map, nutri_map)

    # 4. !! 특수 영양제 투입 X : 리브로수 높이가 2 이상 리브로수는 높이 2를 베어 잘라낸 리브로수로 특수 영양제 구매, 해당 위치에 특수 영양제 존재
    tree_map, nutri_list = buy_nutri(nutri_map, tree_map)
    nutri_map = set_nutri_map(nutri_list)
    if DBG :
        print("4. DONE")
        print_tree_map(tree_map, nutri_map)

    # 년수가 모두 지나고 남아있는 리브로수의 높이들의 총 합을 구함
    if DBG:
        print(f"\n>> {mi} Tree num")
        print(count_trees(tree_map))
############################################################
print(count_trees(tree_map))

# 년수가 모두 지나고 남아있는 리브로수의 높이들의 총 합을 구함