n = int(input())

def divisible_by_12(limit):
    for i in range(0, limit + 1, 12):
        yield i

first = True
for x in divisible_by_12(n):
    if not first:
        print(" ", end="")
    print(x, end="")
    first = False
print()
