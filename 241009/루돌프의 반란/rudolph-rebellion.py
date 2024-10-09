# 아래 r, 오른쪽 c
# 좌상단 (1, 1)
# NxN
# N: 게임판의 크기 (3≤N≤50)
# M: 게임 턴 수 (1≤M≤1000)
# P: 산타의 수 (1≤P≤30)
# C: 루돌프의 힘 (1≤C≤N) 1
# D: 산타의 힘 (1≤D≤N) 2
# 8 14 15 12 12 

# 존나 모르겠는데 잘못된게 없는데...?

# import sys
# sys.stdin = open('C:\\Users\\정선\\Desktop\\ps_study\\정선\\python\\codetree\\example.txt', "r")

# 입력 ####################################
N, M, P, C, D = map(int, input().split())
rr, rc = map(int, input().split())
rr -= 1
rc -= 1
                  
santas = []
for _ in range(P) :
    sn, sr, sc = map(int, input().split())
    santas.append([sn, sr-1, sc-1])
    # 얘가 빠져서 그랬군!
santas.sort(key=lambda x : (x[0]))
for i in range(P) :
    santas[i].pop(0)

santa_status = [-1 for _ in range(P)] # < K 정상, > K 탈락#
scores = [0 for _ in range(P)]
############################################

# 범위, 산타 살아있는지 등 고려 필요 ############################
def br(str) : return f"\033[041m{str}\033[000m" # 산타
def bg(str) : return f"\033[042m{str}\033[000m" # 루돌프
def by(str) : return f"\033[043m{str}\033[000m" # 기절
def bb(str) : return f"\033[044m{str}\033[000m" # 사망

def print_mmap(k) :
    mmap = [[0 for _ in range(N)] for _ in range(N)]
    for r, mm in enumerate(mmap) :
        for c, m in enumerate(mm) :
            flag = False
            for si, (sr, sc) in enumerate(santas) :
                if [sr, sc] == [r, c] :
                    flag = True
                    if santa_status[si] == M + 1 :
                        print(f"{bb(si+1)}", end=" ")
                    elif santa_status[si] < k :
                        print(f"{br(si+1)}", end=" ")
                    else :
                        print(f"{by(si+1)}", end=" ")
                    break
            if [r, c] == [rr, rc] :
                print(f"{bg('R')}", end=" ")
            elif flag == False :
                print(m, end=" ")
        print()
########################################################

def cal_distance(r1, c1, r2, c2) :
    return (r1-r2) * (r1-r2) + (c1-c2) * (c1-c2)

def find_closest_santa(rr, rd, santas, k) :
    # 루돌프 가장 가까운 산타로 돌진, 단 탈락 X
    # 그냥 sort로 하면 되잖아
    infos = [] # santa_nums, distance, r, c
    
    for i, (sr, sc) in enumerate(santas) :
        if santa_status[i] < M + 1 :
            d = cal_distance(rr, rd, sr, sc)
            infos.append([i, d, sr, sc])

    infos.sort(key=lambda x:(x[1], -x[2], -x[3]))
    return infos[0][0]

def check_in_range(r, c) :
    if 0 <= r < N and 0 <= c < N :
        return True
    return False

def move_rudolph(si, rr, rc, k) :
    # (2)
    # 상하좌우대각선 이동 가능(대각선도 1칸)
    # 가장 우선순위 높은 산타로 가장 가까워지는 방향으로 한칸 돌진
    sr, sc = santas[si]
    dr = (int((sr - rr) / abs(sr - rr))) if (sr - rr) else 0
    dc = (int((sc - rc) / abs(sc - rc))) if (sc - rc) else 0

    if [rr + dr, rc + dc] == santas[si] :
        crash(si, [dr, dc], 'r', k)
    return rr + dr, rc + dc

def move_santas(k) :
    # (3)
    # 1-P 순서대로 이동
    # 기절/탈락 이동 X
    # 루돌프에게 가장 가까워지는 방향으로 1칸
    # 다른 산타/게임판 밖 이동X
    # 움직일 수 있는 칸 X -> 이동 X
    # 루돌프 가까워질 방법 X -> 이동 X
    # 상하좌우 이동 가능, 방향이 여러개면 상우하좌 순
    
    # 길이 최소를 구한 다음에 다시 for문을 돌려야되나?
    # 산타는 길이 최소 구할 필요 없는거 같은데....
    # 상우하좌만 지키면 되는거 아냐?
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    for i in range(P) :
        cases = []
        if santa_status[i] < k :
            sr, sc = santas[i]
            d = cal_distance(sr, sc, rr, rc)

            for i_d, (dr, dc) in enumerate(directions) :
                nr = sr + dr
                nc = sc + dc
                if check_in_range(nr, nc) :
                    nd = cal_distance(nr, nc, rr, rc)
                    if nd < d :
                        cases.append([nd, i_d])

            cases.sort(key=lambda x:(x[0], x[1]))

            # print(f"Santa {i+1} case {cases}")

            for (_, i_d) in cases :
                dr, dc = directions[i_d]
                if [sr+dr, sc+dc] not in santas :
                    santas[i] = [sr+dr, sc+dc] 
                    if [sr+dr, sc+dc] == [rr, rc] :
                        crash(i, [-dr, -dc], 's', k)
                    break

def interactive(si, sr, sc, dr, dc) :
    for i, santa in enumerate(santas) :
        # i번째와 산타 부딪힘
        if si != i and [sr, sc] == santa :
            # print(f"Interactive {i+1} [{sr}, {sc}]")
            sr += int(dr / abs(dr)) if dr else 0
            sc += int(dc / abs(dc)) if dc else 0
            if not check_in_range(sr, sc) :
                santa_status[i] = M + 1
                # print(f"BYE {i+1} SANTA")
                santas[i] = [-1, -1]
                return
            else :
                # print(f"산타 밀어냄 {i+1} [{sr}, {sc}]")
                santas[i] = [sr, sc]
                return
                # interactive(si, sr, sc, dr, dc)


def crash(si, drct, who, k) :
    # print(f"!!! 충돌 {who}-{si+1}가 {(santas[si][0], santas[si][1])}에서")
    # (4)
    # 산타, 루돌프 같은 칸 : 충돌
    # 루돌프 움직여 충돌 -> 산타 C 점수, 산타 루돌프 이동방향으로 C칸 밀림
    # 산타 움직여 충돌 -> 산타 D 점수, 산타 자신 반대방향 D칸
    santa_status[si] = k + 1

    sr, sc = santas[si]
    # 으아아아아아악
    if who == 's' :
        score = D
    else :
        score = C
    dr, dc =[drct[0], drct[1]]

    # 밀려날 땐 충돌 X
    # 게임판 밖 => 탈락
    # 다른 산타 존재 : 상호작용
    scores[si] += score
    sr += dr * score
    sc += dc * score

    if check_in_range(sr, sc) :
        interactive(si, sr, sc, dr, dc)
        santas[si] = [sr, sc]
    else :
        santa_status[si] = M + 1
        santas[si] = [-1, -1]
        return

def check_all_santa_lose_and_add_score() :
    flag = True
    for i, ss in enumerate(santa_status) :
        if ss < M+1 :
            flag = False
            scores[i] += 1
    return flag

# (1)
# M개 턴, 매 턴마나 루돌프와 산타들이 한번씩 이동
# 루돌프 이동 -> 1번~P번까지 순서대로 이동, 단 기절/격자 밖 산타 이동X
# (6)
# 충돌 k턴, k+1턴까지 기절, k+2부터 정상
# 기절 시 이동 X, 충돌/상호작용으로 밀려날 수 있음
# 기절 산타 돌진 대상 선택 가능
for k in range(M) :
    # print(f"\n\nROUND {k}")
    # print(" ".join(map(str, scores)))
    # print()
    # print_mmap(k)

    # 젤 가까운 산타 찾기
    cloest_si = find_closest_santa(rr, rc, santas, k)
    # 루돌프 이동
    rr, rc =  move_rudolph(cloest_si, rr, rc, k)
    # print(f"MOVE 루돌프 -> {cloest_si+1}, ({rr, rc})")
    # print_mmap(k)
    # 산타 이동
    move_santas(k)
    # print(f"MOVED 산타들")
    # print(rr, rc)
    # print_mmap(k)

    # (7)
    # M턴 끝나면 종료
    # 산타 모두 탈락, 즉시 종료
    # 매 턴 탈락하지 않은 산타 +1점

    # 턴 끝났을 떄 산타가 얻은 최종점수
    if check_all_santa_lose_and_add_score() :
        break
    # print("END SCORE")
    # print(" ".join(map(str, scores)))
    # print()

print(" ".join(map(str, scores)))