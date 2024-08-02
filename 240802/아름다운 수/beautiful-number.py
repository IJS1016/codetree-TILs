# 1~4 해당 숫자만큼 연달아 같은 숫자가 나오는게 아름다운 수
# n자리 수 중 아름다운 수 개수
N = int(input())

result = 0

def make_num(n_str) :
    global result
    if len(n_str) == N :
        # print("NUM")
        # print(n_str)
        i = 0
        while (i < len(n_str)) :
            s = n_str[i]
            si = int(s)
            if i+si <= N and n_str[i:i+si] == s * int(s) :
                # print("CHECK")
                # print( i+si < N, n_str[i:i+si] == s * int(s) )
                # print(i, i+si)
                i += si
            else :
                # print("BREAK")
                break
        if i == N :
            # print("ADD RESULT")
            result += 1
        return
    for i in range(1, 5) :
        make_num(n_str + str(i))

make_num('')
print(result)