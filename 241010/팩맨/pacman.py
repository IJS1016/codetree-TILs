# https://www.codetree.ai/training-field/frequent-problems/problems/pacman/description?page=2&pageSize=20
# 10.10 17:23
# 팩맨
# import sys
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")

# INPUTS ###########################################################################
import copy

N = 4
M, T = map(int, input().split())
pr, pc = map(int, input().split())
pr, pc = pr-1, pc-1

def init_mon_dict() :
    mon_dict = {}
    for i in range(N) :
        for j in range(N) :
            mon_dict[f"{i}.{j}"] = []
    return mon_dict

def init_mon_mmap(mon_dict) :
    mon_mmap = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            mon_mmap[i][j] = len(mon_dict[f"{i}.{j}"])
    return mon_mmap

mon_dict = init_mon_dict()

# 시계 반대 방향이면, +1 씩 이동하면 됨
mon_drcts = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]
# 상하좌우 우선순위
pac_drcts = [[-1, 0], [1, 0], [0, -1], [0, 1]]

for _ in range(M) :
    r, c, d = map(int, input().split())
    mon_dict[f"{r-1}.{c-1}"].append(d-1)

# mon mmap 초기화(몬스터 복제할 때 사용)
mon_mmap = init_mon_mmap(mon_dict)
dead_mmap = [[0 for _ in range(N)] for _ in range(N)]
###################################################################################

# FUNC  ###########################################################################
def check_in_range(r, c) :
    return 0 <= r < N and 0 <= c < N

def move_monster(t) :
    new_mon_dict = init_mon_dict()

    #    가진 방향대로 한칸 이동
    for r in range(N):
        for c in range(N):
            for mdi in mon_dict[f"{r}.{c}"] :
                #    움직이려는 칸에 몬스터 시체, 팩맨 있거나 격자 벗어나는 경우 반시계 방향으로 45도 이동, 가능할 때까지 회전
                flag = False
                #    8 방향 모두 확인, 움직일 수 없으면 이동 X
                for tdi in range(8) :
                    dr, dc = mon_drcts[(mdi+tdi) % 8]
                    nr, nc = r+dr, c+dc
                    if check_in_range(nr, nc) and [pr, pc] != [nr, nc] and dead_mmap[nr][nc] < t :
                        #    기존 방향도 바뀌게 됨
                        new_mon_dict[f"{nr}.{nc}"].append(mdi+tdi)
                        flag = True
                        break
                if not flag :
                    new_mon_dict[f"{r}.{c}"].append(mdi)

    return new_mon_dict

def get_move_log(r, c, mn, log, visited) :
    # 재귀함수로 list 뱉어내기
    # 만약 방문한 곳도 들린다고 하면, mmap을 계속 갱신해줘야할텐데?
    # visited로 밀고나가는게 나을수도?
    # sort 후 맨 앞에 것으로 몬스터 먹기
    global move_infos
    for i, (dr, dc) in enumerate(pac_drcts) :
        nr, nc = r+dr, c+dc
        # range 초과, 방문하지 않았는지 확인
        if check_in_range(nr, nc) and not visited[nr][nc] :
            # 이동 후,
            #   몬스터 먹은 개수 더하고, 상하좌우 track log 저장
            nmn = mn + len(mon_dict[f"{nr}.{nc}"])

            new_log = copy.deepcopy(log)
            new_log.append(i)

            #   visited True 변경해 넘겨줘야함 => 넘기려면 copy 해야되자나..
            new_visited = copy.deepcopy(visited)
            new_visited[nr][nc] = True

            if len(new_log) == 3:
                move_infos.append([nmn, new_log])
            # 3번 이동 완료 시에만 global list에 더해주기
            else :
                get_move_log(nr, nc, nmn, new_log, new_visited)

def move_packman(move_info, t) :
    global pr, pc
    #    팩맨 총 3칸 이동, 각 이동마다 상하좌우
    #    4가지의 방향을 3칸 이동하기 때문에 총 64개의 이동 방법
    #    가장 많이 먹을 수 있는 방향 여러개 - 상하좌우 우선순위
    #    이동 시 격자 바깥을 나가는 경우 고려 X
    #    이동하는 칸 몬스터 먹어치운 뒤, 몬스터 시체를 남김
    #    알은 먹지 않고, 움직이기 전 함께 있던 몬스터도 먹지 X
    for di in move_info[1] :
        dr, dc = pac_drcts[di]
        pr += dr
        pc += dc
        dead_mmap[dr][dc] = t+2
        mon_dict[f"{pr}.{pc}"] = []

####################################################################################

####################################################################################
# DBG
def print_monster() :
    for r in range(N):
        for c in range(N):
            print(len(mon_dict[f"{r}.{c}"]), end=" ")
        print()

####################################################################################

# 턴
for t in range(1, T+1) :
    # 1. 몬스터 복제 시도
    #    현재의 위치에서 자신과 같은 방향을 가진 몬스터를 복제
    #    알로 부화되지 않은 상태로 움직 X, 나중에 턴 종료할 때 돌면서 추가해주면 됨
    egg_dict = copy.deepcopy(mon_dict)

    # 2. 몬스터 이동
    mon_dict = move_monster(t)

    # 3. 팩맨 이동
    move_infos = []
    visited = [[False for _ in range(N)] for _ in range(N)]
    get_move_log(pr, pc, 0, [], visited)
    # print(move_infos)
    move_infos.sort(key=lambda x:(-x[0], x[1][0], x[1][1], x[1][2]))
    # print(move_infos)
    move_packman(move_infos[0], t)
    # 4. 몬스터 시체 소멸
    #    2턴 동안 몬스터 시체 유지
    #    시체 생긴 후 시체 소멸되기 전까지 2턴을 필요
    # < t으로 사용해서 따로 구현 필요 없음

    # 5. 몬스터 복제 완성
    #    알 형태인 몬스터 부화
    for r in range(N):
        for c in range(N):
            mon_dict[f"{r}.{c}"].extend(egg_dict[f"{r}.{c}"])

result = 0
for r in range(N):
    for c in range(N):
        result += len(mon_dict[f"{r}.{c}"])
# print_monster()
print(result)