# Inheritance allows one class to reuse code from another class.
# The child class gets all methods and properties of the parent class.

class Animal:
    def speak(self):
        print("The animal makes a sound.")

# Dog inherits from Animal
class Dog(Animal):
    pass  # pass means we are not adding anything new for now

# Create object of Dog
my_dog = Dog()

# Even though Dog has no speak() method,
# it can use it because it inherited from Animal.
my_dog.speak()
