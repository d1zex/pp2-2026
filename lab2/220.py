n = int(input())
doc = {}

for _ in range(n):
    command = input().split()
    if command[0] == "set":
        _, key, value = command
        doc[key] = value
    elif command[0] == "get":
        _, key = command
        if key in doc:
            print(doc[key])
        else:
            print(f"KE: no key {key} found in the document")
