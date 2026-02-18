# __init__ is a special method called automatically
# when we create a new object.
# It is used to initialize (set up) object data.
class Student:

    def __init__(self, name, age):
        # self.name and self.age are object variables
        self.name = name
        self.age = age

    def show_info(self):
        print("Name:", self.name)
        print("Age:", self.age)

# Create objects
student1 = Student("Arsen", 20)
student2 = Student("Alua", 21)

# Show information
student1.show_info()
print()
student2.show_info()
