# INPUT ########################################################
import sys
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")

DBG = False
score = 0

N, M, H, K = map(int, input().split())

runner_dict = {} # "x.y" 포맷으로 d 정보 저장
# runner_dict 초기화
for x in range(N) :
    for y in range(N) :
        runner_dict[f"{x}.{y}"] = []

# runners 개수 표시 mmap
runners_mmap = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(M) :
    x, y, d = list(map(int, input().split()))
    runner_dict[f"{x-1}.{y-1}"].append(d)
    runners_mmap[x-1][y-1] += 1

trees = [] # x, y
trees_mmap = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(H) :
    x, y = list(map(int, input().split()))
    trees_mmap[x-1][y-1] += 1

# 술래 위치 정의(정중앙, 방향 위)
fx, fy = N//2, N//2
fd = 0
opt = 0 # opt 0 달팽이 커지는, 1이면 달팽이 작아지는 flag는 0, 0 // N // 2, N // 2

visited = [[False for _ in range(N)] for _ in range(N)]
visited[fx][fy] = True

# 방향 index 정의, 좌우하상
directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
f_directions = [[-1, 0], [0, 1], [1, 0], [0, -1]] # 상우하좌
###############################################################

# DBG  ########################################################
def print_mmap(mmap, map_name='') :
    print(f"## PRINT {map_name} ##")
    for i in range(N) :
        for j in range(N) :
            print(mmap[i][j], end=" ")
        print()

# input 확인
if DBG :
    print_mmap(runners_mmap, map_name='runners_mmap')
    print_mmap(trees_mmap, map_name='trees_mmap')
    print_mmap(visited, map_name='visited')
###############################################################

# FUNC ########################################################
def cal_distance(x1, y1, x2, y2) :
    return abs(x1-x2) + abs(y1-y2)

def check_in_range(x, y) :
    return 0 <= x < N and 0 <= y < N

def change_direction(d) :
    if d < 2 :
        return (d + 1) % 2
    else :
        return (d + 1) % 2 + 2

def get_movable_runner() :
    movable_runners = []
    for i in range(-3, 4) :
        for j in range(-3, 4) :
            # cal_distance(fx, fy, fx + i, fy + j)
            if abs(i) + abs(j) <= 3 :
                if check_in_range(fx + i, fy + j) :
                    movable_runners.append([fx + i, fy + j])
    return movable_runners

def move_runner() :
    # 술래와의 거리가 3 이하인 도망자만 이동
    # 술래와의 거리가 3 이하인 도망자 list 뽑는 함수
    movable_runners = get_movable_runner()
    if DBG :
        print(">>> MOVABLE RUNNERS")
        print(len(movable_runners), movable_runners)

    # 이동 규칙
    new_runner_dict = {}
    for (mrx, mry) in movable_runners:
        new_runner_dict[f"{mrx}.{mry}"] = []

    for (mrx, mry) in movable_runners :
        dn = f"{mrx}.{mry}"
        # 바라보는 칸 1칸 이동, 새롭게 저장하는 dict 만들어야함
        while len(runner_dict[dn]) :
            mrd = runner_dict[dn].pop()
            dx, dy = directions[mrd]
            nx, ny = mrx+dx, mry+dy
            ndn = f"{nx}.{ny}"

            # 격자 벗어나지 않음
            if check_in_range(nx, ny) :
                #   칸 술래 O => 움직 X
                if [nx, ny] == [fx, fy] :
                    new_runner_dict[dn].append(mrd)
                #   칸 술래 X => 움직 O, 나무 무관
                else :
                    new_runner_dict[ndn].append(mrd)

            # 격자 벗어나는 경우
            else :
                # 방향 전환 후 이동
                mrd = change_direction(mrd)
                dx, dy = directions[mrd]
                nx, ny = mrx + dx, mry + dy
                ndn = f"{nx}.{ny}"
                #   칸 술래 O => 움직 X
                if [nx, ny] == [fx, fy] :
                    new_runner_dict[dn].append(mrd)
                #   칸 술래 X => 움직 O, 나무 무관
                else :
                    new_runner_dict[ndn].append(mrd)

    for (mrx, mry) in movable_runners:
        dn = f"{mrx}.{mry}"
        # if DBG :
        #     print(f"MOVED {dn}")
        #     print(f"{runner_dict[dn]} => {new_runner_dict[dn]}")

        runner_dict[dn] = new_runner_dict[dn]
        runners_mmap[mrx][mry] = len(new_runner_dict[dn])

def move_finder() :
    global fx, fy, fd, opt, visited
    # 술래 이동(턴 당 1칸 씩 이동)
    # 위 방향 시작해 달팽이 모양으로 움직
    dx, dy = f_directions[fd]
    fx += dx
    fy += dy
    visited[fx][fy] = True

    if opt == 0 :
        nfd = (fd + 1) % 4
        dx, dy = f_directions[nfd]
        if check_in_range(fx+dx, fy+dy) and not visited[fx+dx][fy+dy] :
            fd = nfd
        if [fx, fy] == [0, 0] :
            fd = 2 # 하로 설정
            opt = 1
            visited = [[False for _ in range(N)] for _ in range(N)]
            visited[0][0] = True

    # 끝까지 오면 거꾸로 중심으로 이동(시계방향)
    elif opt == 1:
        if not check_in_range(fx+dx, fy+dy) and visited[fx+dx][fy+dy] :
            fd = (fd + 3) % 4
        if [fx, fy] == [N//2, N//2] :
            fd = 0 # 상으로 설정
            opt = 0
            visited = [[False for _ in range(N)] for _ in range(N)]
            visited[N//2][N//2] = True

    # 이동 후, 이동방향이 틀어지는 지점이면 방향을 바로 틈
    # 이동 양끝 위치에도 방향을 바로 틀어줘야함을 유의

def find_runner() :
    catch_num = 0
    dx, dy = f_directions[fd]
    # 이동 직후, 시야 내에 있는 도망자를 잡음(술래의 시야는 항상 3칸)
    for i in range(3) :
        nx, ny = fx + dx * i, fy + dy * i
        # 나무 존재 칸은 도망자가 보이지 않음(나무 존재 칸만!)
        if not trees_mmap[nx][ny] :
            catch_num += runners_mmap[nx][ny]
            #    도망자는 사라짐
            runners_mmap[nx][ny] = 0
            runner_dict[f"{nx}.{ny}"] = []

    return catch_num
###############################################################

for kn in range(1, K+1) :
    # 도망자 이동
    move_runner()
    # 술래 이동
    move_finder()
    if DBG :
        print(f"!! ROUND {kn}")
        print_mmap(runners_mmap, map_name='runners_mmap')
        print_mmap(visited, map_name='visited')
    #
    # 도망자 잡기, 도망자를 제거해주는 것도 해줌
    catch_num = find_runner()

    # t번째 턴에 (t x 턴 도망자 수) 만큼의 점수를 얻음
    score += catch_num * kn

print(score)