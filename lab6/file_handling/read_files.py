# Read file content
with open("sample.txt", "r") as file:
    content = file.read()

print("File Content:\n")
print(content)

# line by line
with open("sample.txt", "r") as file:
    lines = file.readlines()

print("Lines:")
for line in lines:
    print(line.strip())