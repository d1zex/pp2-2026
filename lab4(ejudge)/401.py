n = int(input())
def square_generator(limit):
    for i in range(1, limit + 1):
        yield i * i 
for square in square_generator(n):
    print(square)