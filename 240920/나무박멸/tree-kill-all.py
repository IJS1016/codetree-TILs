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

# 끄악 시간 초과...
# 또 시간초과!!!! 갔다와서 수정하기
# 19:21
# 시간초과 어떻게 하지? 백트래킹을 쓸 수가 있나? 모르겠네...
# sort ladmba 사용법 숙지하기
import copy
import sys
DBG = False
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")
if DBG:
    sys.stdin = open('/Users/imjungsun/Desktop/ps_study/정선/python/codetree/example.txt', "r")


N, M, K, C = map(int, input().split())
mmap = []
for _ in range(N) :
    mmap.append(list(map(int, input().split())))

# 방향 선언
udlr_directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
cross_line_directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

def check_in_range(y, x) :
    if 0 <= y < N and 0 <= x < N :
        return True
    return False

def get_tree_coord() :
    tree_coords = []
    for y in range(N) :
        for x in range(N) :
            if mmap[y][x] > 0 :
                tree_coords.append([y, x])
    return tree_coords
                
# 1. 성장
def grow_up_trees() :
    # 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다. 성장은 모든 나무에게 동시에 일어납니다.
    # 나무 좌표만 수행하도록 수정
    for (y, x) in tree_coords :
        for (dy, dx) in udlr_directions :
            ny = y + dy
            nx = x + dx
            if check_in_range(ny, nx) and [ny, nx] in tree_coords :
                mmap[y][x] += 1

def check_dead_space(y, x) :
    for (dcy, dcx, c) in dead_coord :
        if [y, x] == [dcy, dcx] :
            return True
    return False

# 2. 번식
def make_trees(tree_coords) :
    # 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식
    # 동시에 해야되는게...
    tmp_mmap = [[0 for _ in range(N)] for _ in range(N)]
    new_tree_coords = []
    for (y, x) in tree_coords :
        avaliable_coordinates = []
        for d in udlr_directions :
            dy, dx = d
            ny = y + dy
            nx = x + dx
            if check_in_range(ny, nx) and mmap[ny][nx] == 0 and not check_dead_space(ny, nx) : # 범위, 벽, 다른 나무, 제초제 모두 없는 칸에 번식
                avaliable_coordinates.append([ny, nx])
                if [ny, nx] not in new_tree_coords :
                    new_tree_coords.append([ny, nx])
        if len(avaliable_coordinates) :
            tree_num = int(mmap[y][x] / len(avaliable_coordinates))
        for ac in avaliable_coordinates :
            ny, nx = ac
            tmp_mmap[ny][nx] += tree_num
    
    # 번식한거 기존 mmap에 더해주기 
    for (y, x) in new_tree_coords :
        mmap[y][x] += tmp_mmap[y][x]

    tree_coords.extend(new_tree_coords)
    return tree_coords

# 3. 제초제 살포
def put_dead_medicine(tree_coords) :
    # 3. 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제 -> 이것도 나무가 존재하는 위치에 해야되네..
    # 모든 nxn 수행해서 가장 많이 죽는거 완탐
    # 동일할 경우 행이 작은 순서대로, 만약 행이 같은 경우에는 열이 작은 칸에 제초제를 뿌리게 됩니다(y, x 순이 맞음)
    maximum_dead_tree = 0
    maximum_removed_tree_coord = []
    maximum_dead_coord = []

    # DBG
    tree_coords.sort(key = lambda x : (x[0], x[1]))

    for (y, x) in tree_coords :
        before_dead_coord = copy.deepcopy(dead_coord)
        num_dead_tree, removed_tree_coord, tmp_dead_coord = count_dead_tree(y, x, before_dead_coord)
        if num_dead_tree > maximum_dead_tree :
            maximum_dead_tree = num_dead_tree
            maximum_removed_tree_coord = removed_tree_coord
            maximum_dead_coord = tmp_dead_coord

    for (ry, rx) in maximum_removed_tree_coord :
        mmap[ry][rx] = 0

    maximum_tree_coords = []
    for tc in tree_coords :
        if tc not in maximum_removed_tree_coord :
            maximum_tree_coords.append(tc)

    for (rty, rtx) in maximum_removed_tree_coord :
        mmap[rty][rtx] = 0

    return maximum_dead_tree, maximum_tree_coords, maximum_dead_coord

def count_dead_tree(y, x, dead_coord) :
    result = 0
    result += mmap[y][x]  
    removed_tree_coord = [[y, x]]
    dead_coord.append([y, x, C])
    
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
                dead_coord.append([ny, nx, C])
                break
            # 계속 진행
            result += mmap[ny][nx]
            removed_tree_coord.append([ny, nx])
            dead_coord.append([ny, nx, C])

    return result, removed_tree_coord, dead_coord

def pass_year_dead_medicine(dead_coord) :
    new_dead_coord = []
    for (y, x, c) in dead_coord :
        if c > 1 :
            new_dead_coord.append([y, x, c-1])
    return new_dead_coord

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
dead_coord = []
tree_coords = get_tree_coord()

for year in range(M) :
    # print(f"\n\n>>> YEAR {year}")
    if DBG : 
        print(f"\n\n>>> YEAR {year}")
        print("BEFORE GROW UP TREES")
        print_mmap(mmap)
    grow_up_trees()
    if DBG : 
        print("AFTER GROW UP TREES\nBEFOR MAKE TREES")
        print_mmap(mmap)
    tree_coords = make_trees(tree_coords)
    if DBG : 
        print("AFTER MAKE TREES\nBEFORE PUT MEDICINE")
        print_mmap(mmap)
        print(dead_coord)
    dead_coord = pass_year_dead_medicine(dead_coord)
    num_dead_tree, tree_coords, dead_coord = put_dead_medicine(tree_coords)
    if DBG :
        print("AFTER PUT MEDICINE")
        print(f"!!! {num_dead_tree} DEAD TREE")
        print_mmap(mmap)
    result += num_dead_tree
print(result)