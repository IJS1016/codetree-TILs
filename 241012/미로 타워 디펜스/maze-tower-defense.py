# 16:30 풀이 시작
# NxN 나선형 미로, 1,2,3번 몬스터 침략
# 탑에서 몬스터 제거
import sys

# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")

# INPUT #############################################################
# 입력
# 격자 크기 n, 라운드 수 m
N, M = map(int, input().split())
# n+1몬스터 종류(0은 비어있는 칸)
mmap = []
for _ in range(N) :
    mmap.append(list(map(int, input().split())))
# m개의 줄에는 각 라운드마다의 플레이어의 공격 방향 d과 공격 칸 수 p
attack_list = []
for _ in range(M) :
    attack_list.append(list(map(int, input().split())))

MN = 0

score = 0
# 0부터 → ↓ ← ↑
attack_directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
attack_direction_name = ['→', '↓',  '←',  '↑']
#####################################################################

# FUNC  #############################################################
def check_in_range(x, y) :
    return 0 <= x < N and 0 <= y < N

# map이랑 list랑 서로 바꿔주는 함수 생성(map, list 시작부터 끝날때까지)
def list_to_map(m_list) :
    # ← ↓ → ↑
    di = 1
    directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]

    nx, ny = N//2, N//2
    visited = [[False for _ in range(N)] for _ in range(N)]
    visited[nx][ny] = True

    mmap = [[0 for _ in range(N)] for _ in range(N)]
    ny -= 1

    for v in m_list :
        if not check_in_range(nx, ny) :
            break

        mmap[nx][ny] = v
        visited[nx][ny] = True

        # 방향만 바꾸는거
        ndi = (di + 1) % 4
        tdx, tdy = directions[ndi]
        if not visited[nx+tdx][ny+tdy] :
            di = ndi

        dx, dy = directions[di]
        nx, ny = nx + dx, ny + dy

    return mmap

def br() : return "\033[041m"
def bb() : return "\033[000m"

def print_mmap(mmap, x, y) :
    for i, l in enumerate(mmap) :
        s = ""
        for j, v in enumerate(l) :
            if [x, y] == [i, j] :
                s += br()
            s += f"{v} "
            s += bb()
        print(s)

DBG = False
def map_to_list(mmap, m_size=-1) :
    # ← ↓ → ↑
    di = 0
    directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]

    nx, ny = N//2, N//2
    visited = [[False for _ in range(N)] for _ in range(N)]
    result_list = []

    while True :
        # if DBG :
        #     print(nx, ny)
        #     print_mmap(mmap, nx, ny)
        visited[nx][ny] = True
        if mmap[nx][ny] :
            result_list.append(mmap[nx][ny])
        dx, dy = directions[di]
        nx, ny = nx+dx, ny+dy
        if not check_in_range(nx, ny) :
            break
        if (m_size == -1 and mmap[nx][ny] == 0) :
            break
        if m_size > 0 and len(result_list) >= m_size :
            break
        adi = (di + 1) % 4
        adx, ady = directions[adi]
        if check_in_range(nx+adx, ny+ady) and not visited[nx+adx][ny+ady] :
            di = adi

    return result_list

def attack_monster(ad, asize, mmap) :
    global score

    nx, ny = N // 2, N // 2
    dx, dy = attack_directions[ad]
    count = 0

    for s in range(1, asize+1) :
        nx, ny = nx + dx, ny + dy
        if check_in_range(nx, ny) :
            score += mmap[nx][ny]
            if mmap[nx][ny] :
                count += 1
            mmap[nx][ny] = 0

    return mmap, count


def remove_monster(m_list) :
    global score
    flag = False

    m_list.append(0)

    bm = m_list[0]
    result_m_list = []
    si = 0
    con_n = 1

    # 엣지 케이스 대충하지말고, 첨에 생각 잘해서 하기
    # 항상항상 대충 생각해서 나중에 고쳐야지 이러면 큰일 남
    # 처음에 제대로 하기
    # 첫, 끝 처리가 어려운 경우 append로 넣어주는 것도 생각할 수 있음
    for i, m in enumerate(m_list) :
        if i == 0 :
            continue
        if bm == m :
            con_n += 1
        else :
            if con_n >= 4 :
                flag = True
                result_m_list.extend(m_list[si:i-con_n])
                score += con_n * bm
            else :
                result_m_list.extend(m_list[si:i])
            si = i
            bm = m
            con_n = 1
    return result_m_list, flag

def make_monster(m_list) :
    # 개수, 종류대로 생성
    # 새로운 list 만들어서 생성
    # 격자 범위를 넘으면 배열 무시
    result_m_list = []
    m_list.extend([0])

    bm = m_list[0]
    result_m_list = []
    con_n = 1

    for i, m in enumerate(m_list[1:]):
        if bm == m:
            con_n += 1
        else:
            result_m_list.extend([con_n, bm])
            bm = m
            con_n = 1
        if len(result_m_list) >= N*N-1 :
            break

    return result_m_list
#####################################################################

# DEBUG #############################################################
#####################################################################

# MAIN  #############################################################
m_list = map_to_list(mmap)

for R, attack in enumerate(attack_list) :
    # 1. 공격
    # 상하좌우 중 공격칸수만큼 몬스터 공격 가능
    # 비어있는 만큼 빈공간을 채움 => 이걸 어떻게? 개수를 저장해서
    ad, asize = attack
    if DBG:
        print(f">>> Round {R}")
        print("1. BEFORE ATTACK")
        print_mmap(mmap, N//2, N//2)
        print(m_list)
    m_size = len(m_list)
    mmap, acount = attack_monster(ad, asize, mmap)
    if DBG:
        print(f"2. AFTER ATTACK {attack_direction_name[ad]}, {asize}, {acount}")
        print_mmap(mmap, N//2, N//2)
    m_list = map_to_list(mmap, m_size)
    m_size -= acount

    # 3. 제거
    # 미로 위치에서 몬스터 종류가 4번 이상 반복 -> 몬스터 삭제
    # list 이용해서 4번 이상 반복? 삭제
    # 재귀로 반복
    # 이동, 또 4번 반복 삭제
    # 없을 때까지 반복
    if DBG:
        print(f"3. BEFORE REMOVE")
        print(m_list)
    flag = True
    while flag :
        m_list, flag = remove_monster(m_list)

    if DBG:
        print(f"3. AFTER REMOVE")
        print(m_list)
        print(f"Score : {score}")

    # 4. 생성
    m_list = make_monster(m_list)
    if DBG:
        print(f"4. MAKE MONSTER")
        print(m_list)

    mmap = list_to_map(m_list)
    if DBG:
        print_mmap(mmap, N//2, N//2)

print(score)
#####################################################################