# Class methods define behavior (actions) of objects.
class Laptop:

    def __init__(self, brand):
        self.brand = brand

    def turn_on(self):
        print(self.brand, "laptop is turning on.")

    def turn_off(self):
        print(self.brand, "laptop is turning off.")

# Create object
my_laptop = Laptop("Acer")

# Call methods
my_laptop.turn_on()
my_laptop.turn_off()
