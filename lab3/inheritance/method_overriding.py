# Method overriding happens when the child class
# defines a method with the same name as the parent class.

class Vehicle:
    def move(self):
        print("The vehicle is moving.")

class Car(Vehicle):
    # Override the move() method
    def move(self):
        print("The car is driving on the road.")

class Boat(Vehicle):
    # Override the move() method
    def move(self):
        print("The boat is sailing on the water.")

# Create objects
car1 = Car()
boat1 = Boat()

car1.move()
boat1.move()
