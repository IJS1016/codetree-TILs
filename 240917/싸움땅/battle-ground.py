# 9.15 7:43 시작
# nxn 격자
# 각각의 격자에는 무기들이 있을 수 있거나, 빈 격자에 플레이어 위치
# 플레이어 초기 능력치 가짐

# 1-1
# 첫번째 플, 향하는 방향 1칸 이동(격자 벗어나는 경우 반대 방향 1 이동)
# 2-1
# 이동 후 플레이어 존재 X -> 총이 있는지 확인, 총 획득
# 총 가진 경우, 공격력 높은거, 낮은거 내려놓음
# 2-2-1
# 플레이어 존재 O -> 총+능력치 합이 더 큰 플레이어 이김
# 수치 같으면 능력치 큰 애가 이김
# (초기 능력 + 총 공격력 합)의 차이 만큼 포인트 획득
# 2-2-2
# 진 플레이어, 총 내려놓고 방향으로 한칸 이동
# 다른 플레이어, 격자 밖인 경우 오른쪽 90도 회전, 빈칸 보이면 이동
# 총이 있다면, 공격력 높은 총 가지고, 나머지 내려놓음
# 2-2-3
# 이긴 플레이어, 승리칸 총, 원래 총 공격력 높은거 획득, 나머지 내려놓음

# 1번 n번 플레이어 순차적 진행 1라운드 종료
# 포인트 [1, 0, 0, 0] 라운드마다 점수 출력

# n은 격자의 크기, m은 플레이어의 수, k는 라운드의 수
# n개 줄 총의 정보, 총 공격력 의미
# m개 줄 플레이어 정보  y, x, d, s / (y, x)는 플레이어의 위치, d는 방향, s는 플레이어의 초기 능력치
# d 0부터 상우하좌
# 5번쨰 총 공격력
# import sys
# sys.stdin = open("C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt", "r")

# 입력 ############################################################
N, M, K = map(int, input().split())

# 총이 2개인 경우가 있을 수 있으니
mmap = []
for _ in range(N) :
    guns = list(map(int, input().split()))
    line = []
    for g in guns :
        if g == 0 :
            line.append([])
        else :
            line.append([g])
    mmap.append(line)

player_infos = []
for _ in range(M) :
    tmp = list(map(int, input().split())) + [0]
    tmp[0] -= 1
    tmp[1] -= 1
    player_infos.append(tmp)

directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
points = [0 for _ in range(M)]
######################################################################

def check_in_range(y, x) :
    if 0 <= y < N and 0 <= x < N :
        return True
    return False

def move_player(pn) :
    y, x, d, s, g = player_infos[pn]
    if not check_in_range(y + directions[d][0], x + directions[d][1]) :
        d = (d + 2) % 4
    y += directions[d][0]
    x += directions[d][1]
    player_infos[pn] = [y, x, d, s, g]

def act_winner(pn) :
    # 2-2-3
    # 이긴 플레이어, 승리칸 총, 원래 총 공격력 높은거 획득, 나머지 내려놓음
    y, x, d, s, g = player_infos[pn]
    switch_gun(y, x, pn)

def act_loser(pn) :
    # 2-2-2
    y, x, d, s, g = player_infos[pn]
    # 진 플레이어, 총 내려놓고 방향으로 한칸 이동
    if g :
        mmap[y][x].append(g)
        g = 0

    # 다른 플레이어, 격자 밖인 경우 오른쪽 90도 회전, 빈칸 보이면 이동
    ny = y + directions[d][0]
    nx = x + directions[d][1]
    player_infos[pn] = [ny, nx, d, s, 0]

    while not check_in_range(ny, nx) or (check_player_in_the_place(pn) != -1) :
        # 이동을 하고 봐야되는데
        d = (d + 1) % 4
        ny = y + directions[d][0]
        nx = x + directions[d][1]
        player_infos[pn] = [ny, nx, d, s, g]

    # 이동한 곳에 총이 있다면, 공격력 높은 총 가지고, 나머지 내려놓음
    switch_gun(ny, nx, pn)

# 총 바꾸기
def switch_gun(y, x, pn) :
    _, _, _, _, g = player_infos[pn]
    put_guns = mmap[y][x]
    if len(put_guns) :
        if g :
            put_guns = put_guns + [g]
        best_gun = max(put_guns)
        idx = put_guns.index(best_gun)
        put_guns.pop(idx)

    else :
        best_gun = g

    mmap[y][x] = put_guns
    player_infos[pn][-1] = best_gun


def act_with_combat_result(wpn, lpn) :
    x1, y1, d1, s1, g1 = player_infos[wpn]
    x2, y2, d2, s2, g2 = player_infos[lpn]

    t1 = s1+g1
    t2 = s2+g2

    # print(f"Winner {wpn} : {t1}, Loser {lpn} : {t2}")

    # 2-2-2
    # (초기 능력 + 총 공격력 합)의 차이 만큼 포인트 획득
    points[wpn] = t1-t2

    act_loser(lpn)
    # print("** ACT LOSE")
    # print_mmap()
    act_winner(wpn)
    # print("** ACT WINNER")
    # print()

def do_combat(pn1, pn2) :
    # print("||||><><><><><COMBAT><><><><><><|||")
    # 2-2-1
    # 플레이어 존재 O -> 총+능력치 합이 더 큰 플레이어 이김
    x1, y1, d1, s1, g1 = player_infos[pn1]
    x2, y2, d2, s2, g2 = player_infos[pn2]

    t1 = s1+g1
    t2 = s2+g2

    if t1 > t2 : # player1 이김
        act_with_combat_result(pn1, pn2)
    elif t1 < t2 : # player2 이김
        act_with_combat_result(pn2, pn1)
    # 수치 같으면 능력치 큰 애가 이김
    else : 
        if s1 > s2 : # player 1 이김
            act_with_combat_result(pn1, pn2)
        else : # player2 이김
            act_with_combat_result(pn2, pn1)

def check_player_in_the_place(pn) :
    mx, my, md, ms, mg = player_infos[pn]
    for i_pn, player_info in enumerate(player_infos) :
        if i_pn != pn :
            fx, fy, fd, fs, fg = player_info # fixed player
            if [mx, my] == [fx, fy] :
                return i_pn
    return -1

def check_place(pn) :
    y, x, _, _, _ = player_infos[pn]
    # 플레이어 있는지
    other_pn = check_player_in_the_place(pn) 
    if other_pn != -1 :
        # 있으면 싸움
        do_combat(pn, other_pn)
    # 총 있는지 확인
    else :
        switch_gun(y, x, pn)


# DEBUG FUNC #########################################
def br() : return "\033[041m" 
def bb() : return "\033[044m" 
def bg() : return "\033[042m"
def by() : return "\033[043m"
def clear() : return "\033[0m" 
color_list = [br, bb, bg, by]
def print_mmap() :
    for i, pi in enumerate(player_infos) :
        print(color_list[i](), end="")
        print(f"{i}'s GUN POWER : {pi[-1]}", end="")
        print(clear())
    for y, line in enumerate(mmap) :
        for x, v in enumerate(line) :
            for i, p in enumerate(player_infos) :
                py, px, _, _, _ = p
                if [py, px] == [y, x] :
                    print(color_list[i](), end="")
            if len(v) == 0 :
                print("[ ]", end="")
            else :
                print(v, end="")
            print(clear(), end="")
        print()
######################################################


# MAIN ################################################
# print(player_infos)
# print(print_mmap())
for rn in range(K) :
    # print(f">>>>> ROUND <<<<< {rn}")
    for pn in range(M) :
        move_player(pn)
        # print(f"!! MOVE {pn} !!")
        # print_mmap()
        check_place(pn)
    # print(f"\n\n>>>>> END ROUND SCORE<<<<< {rn}")
    # print(points)

print(" ".join(map(str, points)))
######################################################

# 플레이어 번호대로 이동, list 형식으로
# 방향으로
# 범위 벗어났는지 -> 반대 방향으로 전환
# 범위 벗어났는지 -> 반대 방향으로 전환
# 이동
# 플레이어 있는지, 싸움
# 이긴지 봐서 진 애가 총 내려놓고 이동
# 이긴 애가 총 가지고 나머지 내려놓음
# 총 있는지 -> 없으면 총 가지고 있으면 내려놓음(0이면 없고, 1 이상이면 있음)

# 사람 위치는 플레이어 정보 리스트로 하고
# 총만 있도록