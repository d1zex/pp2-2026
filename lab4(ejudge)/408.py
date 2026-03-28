n = int(input())

def primes_up_to(limit):
    for num in range(2, limit + 1):
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                break
        else:
            yield num

print(*primes_up_to(n))
