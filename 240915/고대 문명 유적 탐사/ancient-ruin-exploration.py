# 격자 1개 선택, 반드시 회전 해야함
# 가능한 회전의 방법 중 (1) 유물 1차 획득 가치를 최대화하고, 
# 그러한 방법이 여러가지인 경우 (2) 회전한 각도가 가장 작은 방법을 선택합니다. 
# 그러한 경우도 여러가지인 경우 (3) 회전 중심 좌표의 열이 가장 작은 구간을, 그리고 열이 같다면 행이 가장 작은 구간을 선택합니다.

# 새로운 조각 할당 규칙
# 새로운 조각은 (1) 열 번호가 작은 순으로 조각이 생겨납니다. 
# 만약 열 번호가 같다면 (2) 행 번호가 큰 순으로 조각이 생겨납니다. 
# 단, 벽면의 숫자는 충분히 많이 적혀 있어 생겨날 조각의 수가 부족한 경우는 없다고 가정해도 좋습니다.
# 조각 할당 후, 유물 있으면 계속 취득, 없으면 패스

# 단, 초기에 주어지는 유적지에서는 탐사 진행 이전에 유물이 발견되지 않으며,
# 첫 번째 턴에서 탐사를 진행한 이후에는 항상 유물이 발견됨을 가정해도 좋습니다.

# 코드 구성
# 1
# 회전하는 함수
# 유물 찾는 함수
# 유물 찾고, 새로운 조각 할당 함수 작성
# 유물 찾는 함수
# 없다 Pass
# 다시 1부터 반복
import copy
# import sys
# sys.stdin = open('/Users/imjungsun/Desktop/ps_study/정선/python/codetree/example.txt', "r")

MAP_SIZE = 5
DBG = False

def rotate(y, x, mmap) :
    dyx_infos = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    for _ in range(2) :
        cy, cx = y-1, x-1
        tmp_num = mmap[cy][cx]
        for dyx in dyx_infos :
            for _ in range(2) : 
                cy += dyx[0]
                cx += dyx[1]
                save_num = mmap[cy][cx]
                mmap[cy][cx] = tmp_num
                tmp_num = save_num
            # print("ROTATE")
            # print(cy, cx, tmp_num)
            # print_rotated_mmap(cy, cx, mmap)
            # print()

    return mmap

def check_in_range(y, x) :
    if 0 <= y < 5 and 0 <= x < 5 :
        return True
    return False

def search(y, x, num, visited, history, mmap) :
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    history.append([y, x])
    # print(num, history)
    visited[y][x] = True
    for dirct in directions :
        dy, dx = dirct
        ny = y + dy
        nx = x + dx
        if check_in_range(ny, nx) and not visited[ny][nx] and mmap[ny][nx] == num :
            search(ny, nx, num, visited, history, mmap)
    return history, visited


def find_treasure(mmap) :
    # 상하좌우 있는지 확인
    visited = [[False for _ in range(5)] for _ in range(5)]
    score = 0
    all_history = []
    for y in range(5) :
        for x in range(5) :
            if not visited[y][x] :
                history = []
                history, visited = search(y, x, mmap[y][x], visited, history, mmap)
                if len(history) >= 3 :
                    score += len(history)
                    all_history.extend(history)
    return score, all_history
    

def replace_parts(history, mmap) :
    if DBG :
        print(parts)
    # 열번호가 작은 순서, 행번호가 큰 순서
    sorted_history = sorted(history, key= lambda x : (x[1], -x[0]))
    for y, x in sorted_history :
        mmap[y][x] = parts.pop(0)
    return mmap

def br() : return "\033[041m"  
def bb() : return "\033[044m"  
def bg() : return "\033[042m"    
def bgray() : return "\033[00m"  
def print_mmap(rotated_mmap, history, color) :
    for y, m in enumerate(rotated_mmap) :
        tmp = ''
        for x, n in enumerate(m) :
            if [y, x] in history :
                tmp += color()
                tmp += f"{n} "
                tmp += bgray()
            else :
                tmp += f"{n} "
        print(tmp)

def print_rotated_mmap(ry, rx, rotated_mmap) :
    for y, m in enumerate(rotated_mmap) :
        tmp = ''
        for x, n in enumerate(m) :
            if (abs(ry-y)) <= 1 and abs(rx-x) <= 1:
                tmp += bb()
                if ry==y and rx==x :
                    tmp += br()  
                tmp += f"{n} "
                tmp += bgray()
            else :
                tmp += f"{n} "
        print(tmp)

def get_score() :
    max_score = 0
    best_history = []
    max_angle_condition = 4
    best_mmap = copy.deepcopy(mmap)
    # 최대 점수 조건 저장하고 있기, (3) 회전 중심 좌표의 열이 가장 작은 구간을, 그리고 열이 같다면 행이 가장 작은 구간을 선택 충족
    for x in range(1, MAP_SIZE-1) :
        for y in range(1, MAP_SIZE-1) :
            rotated_mmap = copy.deepcopy(mmap)
            # print("ORIGINAL MMAP")
            # print_rotated_mmap(-10, -10, mmap)
            # print("ROTATED")
            for i in range(3) :
                rotated_mmap = rotate(y, x, rotated_mmap)
                # if DBG :
                #     print_rotated_mmap(y, x, rotated_mmap)
                score, history = find_treasure(rotated_mmap)
                if DBG :
                    if len(history) != 0 :
                        print(f"FIND 보물 ({y}, {x}) - {i}")
                        print_mmap(rotated_mmap, history, br)
                # 그러한 방법이 여러가지인 경우 (2) 회전한 각도가 가장 작은 방법을 선택합니다. 
                if score != 0 and max_score == score :
                    if max_angle_condition > i :
                        best_history = history
                        max_score = score
                        max_angle_condition = i
                        best_mmap = copy.deepcopy(rotated_mmap)
                        if DBG :
                            print(f"BEST Score : {score}")
                if max_score < score :
                    best_history = history
                    max_score = score
                    max_angle_condition = i
                    best_mmap = copy.deepcopy(rotated_mmap)
                    if DBG :
                        print(f"BEST Score : {score}")


    replaced_mmap = replace_parts(best_history, best_mmap)
    if DBG :
        print("REPLACED MAP")
        print_mmap(replaced_mmap, best_history, bg)
    while True :
        score, history = find_treasure(replaced_mmap)
        if DBG :
            print("FIND TREASURE")
            print_mmap(replaced_mmap, history, br)
        if score == 0 :
            break
        max_score += score
        
        replaced_mmap = replace_parts(history, replaced_mmap)
        if DBG : 
            print("REPLACED MAP")
            print_mmap(replaced_mmap, history, bg)
    
    # print(f"!!! MAX {max_score}\n\n")

    return replaced_mmap, max_score
    

# 입력
K, M = map(int, input().split())
mmap = []
for _ in range(5) :
    mmap.append(list(map(int, input().split())))
parts = list(map(int, input().split()))
result = []

for _ in range(K):
    mmap, max_score = get_score()
    if max_score != 0 :
        result.append(str(max_score))
    else :
        break
print(" ".join(result))