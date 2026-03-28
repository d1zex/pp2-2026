lst = input().split()
n = int(input())

def limited_cycle(lst, times):
    for _ in range(times):
        for item in lst:
            yield item

print(*limited_cycle(lst, n))
