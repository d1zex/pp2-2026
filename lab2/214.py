from collections import Counter

n = int(input())
arr = list(map(int, input().split()))

count = Counter(arr)
max_freq = max(count.values())
most_freq = [k for k, v in count.items() if v == max_freq]

print(min(most_freq))
