n = int(input())

def countdown(n):
    for i in range(n, -1, -1):
        yield i

for num in countdown(n):
    print(num)
