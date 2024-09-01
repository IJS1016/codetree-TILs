import sys
# sys.stdin = open(r"C:\Users\정선\Desktop\코테\example1.txt", "r")
# sys.stdin = open(r"C:\Users\정선\Desktop\코테\example2.txt", "r")
# sys.stdin = open(r"C:\Users\정선\Desktop\코테\example3.txt", "r")

N, M, C = map(int, input().split())
mmap = []

for _ in range(N) :
    mmap.append(list(map(int, input().split())))

def cal_value(objects) :
    result = 0
    for v in objects :
        result += v * v
    return result

def get_value(objects) :
    global tmp_maximum
    if sum(objects) > C :
        for i in range(len(objects)) :
            copied_objects = objects.copy()
            del copied_objects[i]
            get_value(copied_objects)
    else :
        tmp = cal_value(objects) 
        if tmp_maximum < tmp :
            tmp_maximum = tmp

maximum = 0
line_maximums = []
for y, line in enumerate(mmap) :
    line_maximum = 0
    for sp in range(N-M+1) :
        tmp_maximum = 0
        get_value(line[sp:sp+M])
        tmp = tmp_maximum
        second_maximum = 0
        for ssp in range(sp+M, N-M+1) :  
            tmp_maximum = 0
            get_value(line[ssp:ssp+M])
            second_tmp = tmp_maximum
            if second_tmp > second_maximum :
                second_maximum = second_tmp
        
        line_total = tmp + second_maximum 
        if line_total > maximum :
            maximum = line_total

        if line_maximum < tmp:
            line_maximum = tmp
        if line_maximum < second_maximum :
            line_maximum = second_maximum
    line_maximums.append(line_maximum)

# 다른 라인에서 뽑았을 때
diff_line_maximum = sum(sorted(line_maximums)[-2:])
if maximum < diff_line_maximum :
    maximum = diff_line_maximum
print(maximum)

# 148