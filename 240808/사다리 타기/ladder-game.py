import sys
limit_number = 15000
sys.setrecursionlimit(limit_number)

N, M = map(int, input().split())
infos = [list(map(int, input().split())) for _ in range(M)]
mix_num = M

max_b = 15

# 형식을 변경하지 않고 바로 받도록 수정
# 메모리 leak 되는 부분 있는지 확인해보기

def convert_info(tmp_infos) :
    infos = []
    # infos[y] = [a1, a2, a3]
    for i in range(1, max_b+1) :
        tmp = []
        for ti in tmp_infos :
            if ti[1] == i :
                tmp.append(ti[0])
        infos.append(tmp)
    return infos

def get_result(infos) :
    infos = convert_info(infos)
    result = []
    for i in range(N) :
        nx = i
        for ny in range(max_b) :
            if nx + 1 in infos[ny] :
                nx += 1
            elif nx in infos[ny] :
                nx -= 1
        result.append(nx)
    return result

# 변수 중복으로 쓴게 있는지 확인
def put_line(tmp_infos, idx) :
    global mix_num

    tmp_result = get_result(tmp_infos)
    if result == tmp_result :
        if mix_num > len(tmp_infos) :
            mix_num = len(tmp_infos)
            return 

    for i, info in enumerate(infos[idx:]) :
        put_line(tmp_infos + [info], idx+i+1)

result = get_result(infos)
# print(result)
put_line([], 0)
print(mix_num)