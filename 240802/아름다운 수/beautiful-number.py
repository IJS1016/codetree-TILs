# 1~4 해당 숫자만큼 연달아 같은 숫자가 나오는게 아름다운 수
# n자리 수 중 아름다운 수 개수
N = int(input())

result = 0

def make_num(n_str) :
    if len(n_str) == N :
        for j in range(1, 5) :
            part = str(j) * j
            while part in n_str :
                n_str = n_str.replace(part, '')
        if len(n_str) == 0 :
            result += 1
        return
    for i in range(1, 5) :
        make_num(n_str + str(i))

make_num('')