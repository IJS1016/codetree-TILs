N = int(input())
lines = [list(map(int, input().split())) for _ in range(N)]

def is_overlap(i_line, n_lines) :
    if len(n_lines) == 0 :
        return False

    ix1, ix2 = i_line
    for n_line in n_lines :
        x1, x2 = n_line
        if ((ix1 < x1 and ix2 < x1) or (x1 < ix1 and x2 < ix1)) :
            return False
    return True

result = 0
def find_max_line_wo_overlap(i, n_lines) :
    global result
    if i == N :
        result = max(result, len(n_lines))
        return
    if not is_overlap(lines[i], n_lines) :
        find_max_line_wo_overlap(i+1, n_lines + [lines[i]])
    find_max_line_wo_overlap(i+1, n_lines)

find_max_line_wo_overlap(0, [])

print(result)