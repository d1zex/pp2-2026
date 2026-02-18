# sorted() can use lambda to define custom sorting logic.
students = [
    ("Arsen", 85),
    ("Alua", 92),
    ("VEniamin", 78),
    ("Gabiden", 95)
]

# Sort students by their score (second value in tuple)
sorted_students = sorted(students, key=lambda student: student[1])

print("Sorted by score (ascending):")
print(sorted_students)


# Sort in descending order
sorted_students_desc = sorted(students, key=lambda student: student[1], reverse=True)

print("\nSorted by score (descending):")
print(sorted_students_desc)
