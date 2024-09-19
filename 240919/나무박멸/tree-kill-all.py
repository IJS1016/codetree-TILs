# 179

# 17:01 문풀 시작
# nxn 격자, 나무 그루 수, 벽 정보
# 제초제 k 범위만큼 대각선으로 퍼짐, 벽이 있는 경우 가로막혀 전파되지 않음
# 1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다. 성장은 모든 나무에게 동시에 일어납니다.
# 2. 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행
# 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행합니다.
# 이때 각 칸의 나무 그루 수에서 총 번식이 가능한 칸의 개수만큼 나누어진 그루 수만큼 번식이 되며, 나눌 때 생기는 나머지는 버립니다. 
# 번식의 과정은 모든 나무에서 동시에 일어나게 됩니다.
# 번식 시 겹치면 더해짐
# 3. 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제
# 나무 있는 칸 4개 대각선 방향, k칸 만큼 전파, 뿌려지고 C년까지 남아있음
# 벽 있거나, 나무 없는 경우 그 칸까지 제초제 뿌려지고, 이후로 전파 X, C년까지 남아있다가 C+1년째에 사라짐
# 새로 뿌려지면 다시 C년 동안 유지

# 번식하고, 제초제 뿌릴 때 C년이 되면 제조체 사라짐

# 입력 ########################################
# 첫 번째 줄에 격자의 크기 n, 
# 박멸이 진행되는 년 수 m, 
# 제초제의 확산 범위 k, 
# 제초제가 남아있는 년 수 c
# 이후 n개의 줄에 걸쳐 각 칸의 나무의 그루 수, 벽의 정보가 주어집니다. 
# 총 나무의 그루 수는 1 이상 100 이하의 수로, 빈 칸은 0, 벽은 -1으로 주어지게 됩니다.
# 5 ≤ n ≤ 20
# 1 ≤ m ≤ 1000
# 1 ≤ k ≤ 20
# 1 ≤ c ≤ 10
import copy
import sys
DBG = False
if DBG:
    sys.stdin = open('/Users/imjungsun/Desktop/ps_study/정선/python/codetree/example.txt', "r")


N, M, K, C = map(int, input().split())
mmap = []
for _ in range(N) :
    mmap.append(list(map(int, input().split())))
mmap_dead = [[0 for _ in range(N)] for _ in range(N)]

# 방향 선언
udlr_directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
cross_line_directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

def check_in_range(y, x) :
    if 0 <= y < N and 0 <= x < N :
        return True
    return False

# 1. 성장
def grow_up_trees() :
    # 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다. 성장은 모든 나무에게 동시에 일어납니다.
    for y in range(N) :
        for x in range(N) :
            if mmap[y][x] > 0 :
                for d in udlr_directions :
                    dy, dx = d
                    ny = y + dy
                    nx = x + dx
                    if check_in_range(ny, nx) and mmap[ny][nx] > 0 :
                        mmap[y][x] += 1

# 2. 번식
def make_trees() :
    # 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식
    # 동시에 해야되는게...
    # debug 용
    if DBG : history_coor = []

    tmp_mmap = [[0 for _ in range(N)] for _ in range(N)]
    for y in range(N) :
        for x in range(N) :
            if mmap[y][x] > 0 :
                avaliable_coordinates = []
                for d in udlr_directions :
                    dy, dx = d
                    ny = y + dy
                    nx = x + dx
                    if check_in_range(ny, nx) and mmap[ny][nx] == 0 and mmap_dead[ny][nx] == 0 : # 범위, 벽, 다른 나무, 제초제 모두 없는 칸에 번식
                        avaliable_coordinates.append([ny, nx])
                        if DBG : history_coor.append([ny, nx])
                if len(avaliable_coordinates) :
                    tree_num = int(mmap[y][x] / len(avaliable_coordinates))
                for ac in avaliable_coordinates :
                    ny, nx = ac
                    tmp_mmap[ny][nx] += tree_num
    
    # 번식한거 기존 mmap에 더해주기 
    for y in range(N) :
        for x in range(N) :
            mmap[y][x] += tmp_mmap[y][x]

# 3. 제초제 살포
def put_dead_medicine() :
    # 3. 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제
    # 모든 nxn 수행해서 가장 많이 죽는거 완탐
    # 동일할 경우 행이 작은 순서대로, 만약 행이 같은 경우에는 열이 작은 칸에 제초제를 뿌리게 됩니다(y, x 순이 맞음)
    maximum_dead_tree = 0
    maximum_mmap = copy.deepcopy(mmap)

    # DBG
    dbg_mmap = [[0 for _ in range(N)] for _ in range(N)]
    max_y, max_x = 0, 0
    for y in range(N) :
        for x in range(N) :
            num_dead_tree, tmp_mmap, tmp_mmap_dead = count_dead_tree(y, x)
            dbg_mmap[y][x] = num_dead_tree
            if num_dead_tree > maximum_dead_tree :
                maximum_dead_tree = num_dead_tree
                maximum_mmap = tmp_mmap
                maximum_dead_mmap = tmp_mmap_dead
                max_y = y
                max_x = x

    if DBG :
        print("!!!!!!! EXAMPLE NUM DEAD")
        print_mmap(dbg_mmap, [[max_y, max_x]])
    return maximum_dead_tree, maximum_mmap, maximum_dead_mmap

def count_dead_tree(y, x) :
    result = 0
    tmp_mmap = copy.deepcopy(mmap)
    tmp_mmap_dead = copy.deepcopy(mmap_dead)
    if mmap[y][x] > 0 :
        result += mmap[y][x]   
        tmp_mmap[y][x] = 0 
        tmp_mmap_dead[y][x] = C
        for d in cross_line_directions :
                ny = y
                nx = x
                dy, dx = d
                for size in range(K) :
                    ny += dy
                    nx += dx
                    # break 조건들
                    # 범위 벗어난 경우, 벽 있거나
                    if not check_in_range(ny, nx) or mmap[ny][nx] == -1 :
                        break
                    # 나무 없는 경우
                    elif mmap[ny][nx] == 0 :
                        # 제초제 남겨두고 break
                        tmp_mmap_dead[ny][nx] = C
                        break
                    # 계속 진행
                    result += tmp_mmap[ny][nx]
                    tmp_mmap[ny][nx] = 0
                    tmp_mmap_dead[ny][nx] = C

    return result, tmp_mmap, tmp_mmap_dead

def pass_year_dead_medicine() :
    for y in range(N) :
        for x in range(N) :
            if mmap_dead[y][x] > 0 :
                mmap_dead[y][x] -= 1

def bg_color(word, ci) : return f"\033[04{ci}m{word}\033[040m"
def print_mmap(mmap, color_coord=[]) :
    for y in range(N) :
        for x in range(N) :
            margin = " " * (3 - len(str(mmap[y][x])))
            tmp = f"{margin}{mmap[y][x]}"
            for i, coor in enumerate(color_coord) :
                if [y, x] == coor :
                    tmp = bg_color(f"{margin}{mmap[y][x]}", i+1)
                    break
            print(tmp, end=" ")
        print()

result = 0
for year in range(M) :
    if DBG : 
        print(f"\n\n>>> YEAR {year}")
        print("BEFORE GROW UP TREES")
        print_mmap(mmap)
    grow_up_trees()
    if DBG : 
        print("AFTER GROW UP TREES\nBEFOR MAKE TREES")
        print_mmap(mmap)
    make_trees()
    if DBG : 
        print("AFTER MAKE TREES\nBEFORE PUT MEDICINE")
        print_mmap(mmap)
    pass_year_dead_medicine()
    num_dead_tree, mmap, mmap_dead = put_dead_medicine()
    if DBG :
        print("AFTER PUT MEDICINE")
        print(f"!!! {num_dead_tree} DEAD TREE")
        print_mmap(mmap)
        print("DEAD MMAP")
        print_mmap(mmap_dead)
    result += num_dead_tree
print(result)