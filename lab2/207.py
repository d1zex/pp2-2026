n = int(input())
nums = list(map(int, input().split()))

max_val = nums[0]
pos = 1

for i in range(1, n):
    if nums[i] > max_val:
        max_val = nums[i]
        pos = i + 1

print(pos)
