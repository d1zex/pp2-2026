# map() applies a function to every element in a list.
numbers = [1, 2, 3, 4, 5]

# Using lambda to square each number
squared_numbers = map(lambda x: x * x, numbers)

# map returns a map object, so we convert it to list to see results
squared_numbers = list(squared_numbers)

print("Original numbers:", numbers)
print("Squared numbers:", squared_numbers)
