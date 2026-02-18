# Class variables are shared between all objects.
# Object variables are unique for each object.

class Phone:

    # This is a class variable (shared by all phones)
    category = "Electronics"

    def __init__(self, brand):
        # This is an object variable (different for each phone)
        self.brand = brand

# Create objects
phone1 = Phone("Apple")
phone2 = Phone("Samsung")

# Access class variable
print("Phone1 category:", phone1.category)
print("Phone2 category:", phone2.category)

# Access object variables
print("Phone1 brand:", phone1.brand)
print("Phone2 brand:", phone2.brand)
