# Multiple inheritance means a class can inherit
# from more than one parent class.

class Engine:
    def start_engine(self):
        print("Engine started.")

class GPS:
    def find_location(self):
        print("Finding current location...")

# SmartCar inherits from both Engine and GPS
class SmartCar(Engine, GPS):
    pass

# Create object
my_smart_car = SmartCar()

# SmartCar can use methods from both parents
my_smart_car.start_engine()
my_smart_car.find_location()
