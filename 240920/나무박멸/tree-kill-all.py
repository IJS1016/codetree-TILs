# 변수 선언 및 입력:
n, m, k, c = tuple(map(int, input().split()))
tree = [[0] * (n + 1)]
for _ in range(n):
    tree.append([0] + list(map(int, input().split())))

add_tree = [
    [0] * (n + 1)
    for _ in range(n + 1)
]
herb = [
    [0] * (n + 1)
    for _ in range(n + 1)
]

ans = 0


def is_out_range(x, y):
    return not (1 <= x and x <= n and 1 <= y and y <= n)


# 1단계 : 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다.
def step_one():
    dxs, dys = [-1, 0, 1, 0], [0, -1, 0, 1]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if tree[i][j] <= 0: 
                continue

            # 나무가 있는 칸의 수(cnt)만큼 나무가 성장합니다.
            cnt = 0
            for dx, dy in zip(dxs, dys):
                nx, ny = i + dx, j + dy
                if is_out_range(nx, ny): 
                    continue
                if tree[nx][ny] > 0: 
                    cnt += 1

            tree[i][j] += cnt


# 2단계 : 기존에 있었던 나무들은 아무것도 없는 칸에 번식을 진행합니다.
def step_two():
    dxs, dys = [-1, 0, 1, 0], [0, -1, 0, 1]

    # 모든 나무에서 동시에 일어나는 것을 구현하기 위해 하나의 배열을 더 이용합니다.
    # add_tree를 초기화해줍니다.
    for i in range(1, n + 1):
        for j in range(1, n + 1): 
            add_tree[i][j] = 0

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if tree[i][j] <= 0: 
                continue

            # 해당 나무와 인접한 나무 중 아무도 없는 칸의 개수를 찾습니다.
            cnt = 0
            for dx, dy in zip(dxs, dys):
                nx, ny = i + dx, j + dy
                if is_out_range(nx, ny): 
                    continue
                if herb[nx][ny]: 
                    continue
                if tree[nx][ny] == 0: 
                    cnt += 1

            # 인접한 나무 중 아무도 없는 칸은 cnt로 나눠준 만큼 번식합니다.
            for dx, dy in zip(dxs, dys):
                nx, ny = i + dx, j + dy
                if is_out_range(nx, ny): 
                    continue
                if herb[nx][ny]: 
                    continue
                if tree[nx][ny] == 0: 
                    add_tree[nx][ny] += tree[i][j] // cnt
    
    # add_tree를 더해 번식을 동시에 진행시킵니다.
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            tree[i][j] += add_tree[i][j]


# 3단계 : 가장 많이 박멸되는 칸에 제초제를 뿌립니다.
def step_three():
    global ans

    dxs, dys = [-1, 1, 1, -1], [-1, -1, 1, 1]

    max_del, max_x, max_y = 0, 1, 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # 모든 칸에 대해 제초제를 뿌려봅니다. 각 칸에서 제초제를 뿌릴 시 박멸되는 나무의 그루 수를 계산하고,
            # 이 값이 최대가 되는 지점을 찾아줍니다.
            if tree[i][j] <= 0: 
                continue

            cnt = tree[i][j]
            for dx, dy in zip(dxs, dys):
                nx, ny = i, j
                for _ in range(k):
                    nx, ny = nx + dx, ny + dy
                    if is_out_range(nx, ny): 
                        break
                    if tree[nx][ny] <= 0: 
                        break
                    cnt += tree[nx][ny]

            if max_del < cnt:
                max_del = cnt
                max_x = i
                max_y = j

    ans += max_del

    # 찾은 칸에 제초제를 뿌립니다.
    if tree[max_x][max_y] > 0:
        tree[max_x][max_y] = 0
        herb[max_x][max_y] = c

        for dx, dy in zip(dxs, dys):
            nx, ny = max_x, max_y
            for _ in range(k):
                nx, ny = nx + dx, ny + dy
                if is_out_range(nx, ny): 
                    break
                if tree[nx][ny] < 0: 
                    break
                if tree[nx][ny] == 0:
                    herb[nx][ny] = c
                    break

                tree[nx][ny] = 0
                herb[nx][ny] = c


# 제초제의 기간을 1년 감소시킵니다.
def delete_herb():
    for i in range(1, n + 1):
        for j in range(1, n + 1): 
            if herb[i][j] > 0: 
                herb[i][j] -= 1


for _ in range(m):
    # 1단계 : 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다.
    step_one()

    # 2단계 : 기존에 있었던 나무들은 아무것도 없는 칸에 번식을 진행합니다.
    step_two()

    # 제초제의 기간을 1년 감소시킵니다.
    delete_herb()

    # 3단계 : 가장 많이 박멸되는 칸에 제초제를 뿌립니다.
    step_three()

print(ans)