from collections import Counter

n = int(input())
numbers = [input() for _ in range(n)]

count = Counter(numbers)
print(sum(1 for v in count.values() if v == 3))
