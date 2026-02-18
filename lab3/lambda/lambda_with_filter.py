# filter() selects only elements that match a condition.
numbers = [10, 15, 20, 25, 30, 35]

# Keep only numbers greater than 20
filtered_numbers = filter(lambda x: x > 20, numbers)

# Convert to list to see results
filtered_numbers = list(filtered_numbers)

print("Original numbers:", numbers)
print("Numbers greater than 20:", filtered_numbers)
