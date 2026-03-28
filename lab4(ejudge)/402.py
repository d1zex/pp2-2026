n = int(input())

def even_generator(limit):
    for i in range(0, limit + 1, 2):
        yield i

first = True
for x in even_generator(n):
    if not first:
        print(",", end="")
    print(x, end="")
    first = False
print()
