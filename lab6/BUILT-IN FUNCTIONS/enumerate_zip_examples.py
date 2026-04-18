names = ["Ali", "Arman", "Aruzhan"]
scores = [85, 90, 78]

# enumerate
for index, name in enumerate(names):
    print(index, name)

# zip
for name, score in zip(names, scores):
    print(name, score)

# type conversion
num_str = "123"
num_int = int(num_str)
print(type(num_int), num_int)