import copy
# import sys
from collections import deque
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")


# INPUT ################################################
directions = [[0, -1], [-1, 0], [0, 1], [1, 0]] # 좌상우하
N, M, K = map(int, input().split())

mmap = []
for _ in range(N):
    mmap.append(list(map(int, input().split())))

air_locs = []
office_map = [[False for _ in range(N)] for _ in range(N)]
for tx, line in enumerate(mmap) :
    for ty, v in enumerate(line) :
        if v >= 2 :
            air_locs.append([tx, ty, mmap[tx][ty]-2])
        elif v == 1 :
            office_map[tx][ty] = True

wall_map = [[[0, 0] for _ in range(N)] for _ in range(N)]
for _ in range(M):
    x, y, d = list(map(int, input().split()))
    wall_map[x-1][y-1][d] = 1
########################################################

# DEBUG ################################################
DBG = False
direction_name = ['좌','상','우','하']
def br(s) : return f"\033[041m{s}\033[000m"
def bg(s) : return f"\033[042m{s}\033[000m"
def by(s) : return f"\033[043m{s}\033[000m"
def bb(s) : return f"\033[044m{s}\033[000m"

# 순서대로 좌상우하
colors = [br, bg, by, bb]

def print_wall_map() :
    pass

def print_wind_map(mmap, ax=-1, ay=-1, d=0) :
    for tx, line in enumerate(mmap):
        wall_str = ""
        wind_str = ""
        for ty, v in enumerate(line):
            if wall_map[tx][ty][0] : # 위에 벽
                wall_str += "= "
            else :
                wall_str += "  "
            if [ax, ay] == [tx, ty] :
                if ty+1 < N and wall_map[tx][ty+1][1] :
                    wind_str += f"{colors[d](v)}|"
                else :
                    wind_str += f"{colors[d](v)} "
            else :
                if ty+1 < N and wall_map[tx][ty+1][1] :
                    wind_str += f"{v}|"
                else :
                    wind_str += f"{v} "
        print(wall_str)
        print(wind_str)

########################################################

# FUNC  ################################################
def check_in_range(x, y) :
    return 0 <= x < N and 0 <= y < N

def check_block(nx, ny, d) : # 막히면 True, 안막히면 False
    dx, dy = directions[d]
    if d == 0:  # 좌로 이동
        if wall_map[nx][ny][1] :  # 이동 전 위치가 1인 경우 막힘
            return True
    elif d == 1:  # 상로 이동
        if wall_map[nx][ny][0]:  # 이동 전 위치가 0인 경우 막힘
            return True
    elif d == 2:  # 우로 이동
        if wall_map[nx+dx][ny+dy][1] :  # 이동 후 위치가 1인 경우 막힘
            return True
    elif d == 3:  # 하로 이동
        if wall_map[nx+dx][ny+dy][0] :  # 이동 후 위치가 0인 경우 막힘
            return True
    return False

# 디버깅 시, dx, dy 순서 바뀐거 없는지 더블체크
def run_airconditioner(x, y, d) :
    # 0, 1, 2, 3 : 좌상우하
    # 2, 3, 4, 5
    # 2/4이면 1, 3
    # 3/5이면 0, 2
    wind_map = [[0 for _ in range(N)] for _ in range(N)]

    init_score = 5
    if not check_block(x, y, d) :
        dx, dy = directions[d]
        infos = deque([[x+dx, y+dy, init_score]])
        wind_map[x+dx][y+dy] = init_score
    else :
        return wind_map

    if (d % 2) : # 1, 3 => 상하
        sd = [0, 2]
    else : # 0, 2 => 좌우
        sd = [1, 3]

    while len(infos) :
        nx, ny, score = infos.popleft()
        # if DBG : print(nx, ny, score)

        if score == 1 :
            continue

        # 자기 방향으로 한칸 이동 #################################
        # 벽이 있는지 없는지 확인, 상하좌우에 따라 달라짐
        dir_combis = [[d], [sd[0], d], [sd[1], d]]

        for dc in dir_combis :
            available = True
            tx, ty = nx, ny
            for tmp_d in dc :
                dx, dy = directions[tmp_d]

                if not check_in_range(tx+dx, ty+dy) :
                    available = False
                    break
                elif check_block(tx, ty, tmp_d) : #  막히면 True, 안막히면 False
                    available = False
                    break
                tx += dx
                ty += dy
            if available and wind_map[nx][ny] != score-1 :
                infos.append([tx, ty, score-1])
                wind_map[tx][ty] = score-1
                # if DBG :
                #     print(f"!!! ({tx}, {ty}) {score-1}")
                #     print_wind_map(wind_map)
                #     print()

    return wind_map

def add_wind_map(air_map, total_wind_map) :
    for tx in range(N) :
        for ty in range(N) :
            air_map[tx][ty] += total_wind_map[tx][ty]
    return air_map

def get_total_wind_map() :
    total_wind_map = [[0 for _ in range(N)] for _ in range(N)]

    for (x, y, d) in air_locs:
        if DBG:
            print(f"WIND MAP of {x}, {y} {direction_name[d]}")
        wind_map = run_airconditioner(x, y, d)
        for tx in range(N):
            for ty in range(N):
                total_wind_map[tx][ty] += wind_map[tx][ty]
        if DBG:
            print_wind_map(wind_map, x, y, d)
    return total_wind_map

def mix_cool_air(mmap) :
    result_mmap = copy.deepcopy(mmap)

    for tx, line in enumerate(mmap) :
        for ty, air in enumerate(line) :
            for dx, dy in directions :
                nx, ny = tx+dx, ty+dy
                if check_in_range(nx, ny) :
                    tair = mmap[nx][ny]
                    if air > tair :
                        move_air = int(((air - tair) / 4))
                        result_mmap[tx][ty] -= move_air
                        result_mmap[nx][ny] += move_air

    return result_mmap

def reduce_cool_air(mmap) :
    for tx in [0, N-1]:
        for ty in range(N):
            if mmap[tx][ty] > 0 :
                mmap[tx][ty] -= 1

    for ty in [0, N-1]:
        for tx in range(1, N-1):
            if mmap[tx][ty] > 0:
                mmap[tx][ty] -= 1
    return mmap

def check_end_condition(mmap) :
    for tx in range(N):
        for ty in range(N):
            if office_map[tx][ty] and mmap[tx][ty] < K :
                return False
    return True
########################################################



# MAIN  ################################################
# 에어컨 냉방 과정
# 에어컨 위치, 방향 넣어주면 퍼저나가는거 수행하기(맨 처음 턴에만 한번하면 되잖아!)
# 에어컨 위치 찾기 - 이걸 저장해서 턴 지날 때 마다 나중에 계속 더해주기
air_map = [[0 for _ in range(N)] for _ in range(N)]
total_wind_map = get_total_wind_map()

time = 1
end_flag = False
while (time <= 100) :
    # 순서대로
    # 1. 에어컨 냉방
    # total_wind_map 더해주기
    add_wind_map(air_map, total_wind_map)

    if DBG :
        print(">> 1. ADD TOTAL MAP")
        print_wind_map(air_map)

    # 시원한 공기들 섞이기
    air_map = mix_cool_air(air_map)
    if DBG :
        print(">> 2. MIXED AIR MAP")
        print_wind_map(air_map)

    # 시원한 공기 감소
    # 외벽에 있는 칸에 대해서만 시원함이 1씩 감소
    air_map = reduce_cool_air(air_map)

    if DBG :
        print(">> 3. REDUCE AIR")
        print_wind_map(air_map)

    # 에어컨, 벽, 사무실 저장 어떻게 할건지 정해야됨
    if check_end_condition(air_map) :
        end_flag = True
        break
    time += 1

if end_flag :
    print(time)
else :
    print(-1)

########################################################