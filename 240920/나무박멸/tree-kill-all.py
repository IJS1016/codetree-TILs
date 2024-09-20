import copy
import sys
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")

# NxN 모두 돌지 않고, coord 저장해서 필요한거만 돌리도록 하기
#  나눗셈이 존재한다, 0인 경우 반드시 생각해줘야 함
# deepcopy 사용하지 말기 -> 시간 초과
# sort lambda 사용하기
# 디버깅할 때 침착하게 하기
import time
import functools

def measure_time(func):
    @functools.wraps(func)
    def wrapper_measure_time(*args, **kwargs):
        start_time = time.time()  # 시작 시간 기록
        result = func(*args, **kwargs)  # 원래 함수 실행
        end_time = time.time()    # 끝난 시간 기록
        elapsed_time = end_time - start_time  # 소요 시간 계산
        print(f"Function '{func.__name__}' 실행 시간: {elapsed_time:.6f}초")
        return result
    return wrapper_measure_time

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
# @measure_time
def grow_up_trees(tree_coords) :
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

# 아 나머지가 0일때... 제외해줘야되는데... 그러지 않고 new_tree에는 있고 실제 심어지는 나무는 0이라서 제외가 되었군
# 2. 번식
# @measure_time
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
        if len(avaliable_coordinates) :
            tree_num = int(mmap[y][x] / len(avaliable_coordinates))
            
        for ac in avaliable_coordinates :
            ny, nx = ac
            tmp_mmap[ny][nx] += tree_num
            if [ny, nx] not in new_tree_coords and tree_num > 0:
                new_tree_coords.append([ny, nx])
            
    # 번식한거 기존 mmap에 더해주기 
    for (y, x) in new_tree_coords :
        mmap[y][x] += tmp_mmap[y][x]

    tree_coords.extend(new_tree_coords)
    return tree_coords

# 3. 제초제 살포
# @measure_time
def put_dead_medicine(tree_coords, dead_coord) :
    # 3. 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸에 제초제 -> 이것도 나무가 존재하는 위치에 해야되네..
    # 모든 nxn 수행해서 가장 많이 죽는거 완탐
    # 동일할 경우 행이 작은 순서대로, 만약 행이 같은 경우에는 열이 작은 칸에 제초제를 뿌리게 됩니다(y, x 순이 맞음)
    maximum_dead_tree = 0
    maximum_removed_tree_coord = []
    maximum_dead_coord = []

    tree_coords.sort(key = lambda x : (x[0], x[1]))

    for (y, x) in tree_coords :
        # before_dead_coord = copy.deepcopy(dead_coord) # copy 많은 시간...
        num_dead_tree, removed_tree_coord, tmp_dead_coord = count_dead_tree(y, x, dead_coord)
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
        else :
            rty, rtx = tc
            mmap[rty][rtx] = 0

    return maximum_dead_tree, maximum_tree_coords, maximum_dead_coord

# C도 시간초과 줄이기 위해 1로 하지 말고, 연도로 해야함 => 별로 의미 없을거 같은데
def count_dead_tree(y, x, dead_coord) :
    result = 0
    result += mmap[y][x]  
    removed_tree_coord = [[y, x]]
    add_dead_coord = [[y, x, C]]
    
    for d in cross_line_directions :
        ny = y
        nx = x
        dy, dx = d
        for _ in range(K) :
            ny += dy
            nx += dx
            # break 조건들
            # 범위 벗어난 경우, 벽 있거나
            if not check_in_range(ny, nx) or mmap[ny][nx] == -1 :
                break
            # 나무 없는 경우
            elif mmap[ny][nx] == 0 :
                # 제초제 남겨두고 break
                add_dead_coord.append([ny, nx, C])
                break
            # 계속 진행
            result += mmap[ny][nx]
            removed_tree_coord.append([ny, nx])
            add_dead_coord.append([ny, nx, C])

    return result, removed_tree_coord, dead_coord + add_dead_coord

# @measure_time
def pass_year_dead_medicine(dead_coord) :
    new_dead_coord = []
    for (y, x, c) in dead_coord :
        if c > 1 :
            new_dead_coord.append([y, x, c-1])
    return new_dead_coord


result = 0
dead_coord = []

tree_coords = get_tree_coord()

for year in range(M) :
    grow_up_trees(tree_coords)
    tree_coords = make_trees(tree_coords)
    dead_coord = pass_year_dead_medicine(dead_coord)
    num_dead_tree, tree_coords, dead_coord = put_dead_medicine(tree_coords, dead_coord)
    result += num_dead_tree
    len_tree_coord2 = len(tree_coords)

print(result)