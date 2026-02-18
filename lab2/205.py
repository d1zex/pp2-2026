n = int(input())

if n <= 0:
    print("NO")
else:
    while n % 2 == 0:
        n //= 2
    print("YES" if n == 1 else "NO")
