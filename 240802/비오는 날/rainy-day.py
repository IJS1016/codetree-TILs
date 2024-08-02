n = int(input())

class weather_data:
    def __init__(self, d, y, w):
        self.date = d
        self.y = y
        self.weather = w

arr = []

for i in range(n):
    temp = input().split()
    arr.append(weather_data(temp[0], temp[1], temp[2]))

arr.sort(key = lambda x: (-1 if x.weather == "Rain" else 1, int(x.date[0:4]), int(x.date[6:7]), int(x.date[9:10])))
# 1. 비가 오는 날씨일 경우 우선 // 빠른 날짜(낮은 숫자) 순으로 우선 정렬

print(f"{arr[0].date} {arr[0].y} {arr[0].weather}")