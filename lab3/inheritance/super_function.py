# super() allows us to call the parent class method
# inside the child class.
class Person:
    def __init__(self, name):
        self.name = name
        print("Person constructor called")

class Student(Person):
    def __init__(self, name, university):
        # Call parent constructor
        super().__init__(name)
        self.university = university
        print("Student constructor called")

    def show_info(self):
        print("Name:", self.name)
        print("University:", self.university)
# Create object
student1 = Student("Arsen", "KBTU")
student1.show_info()
