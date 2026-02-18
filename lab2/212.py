n = int(input())
arr = list(map(int, input().split()))
arr = [x**2 for x in arr]
print(*arr)
