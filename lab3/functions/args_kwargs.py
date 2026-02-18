# *args allows the function to accept many positional arguments.
# **kwargs allows the function to accept many keyword arguments.

def student_info(*args, **kwargs):
    # args is treated like a tuple
    print("Subjects:")
    for subject in args:
        print("-", subject)

    print("\nAdditional Info:")
    # kwargs is treated like a dictionary
    for key, value in kwargs.items():
        print(key + ":", value)

# Calling the function with multiple arguments
student_info(
    "TNLC",
    "KIP",
    "Programming",
    name="Arsen",
    age=20,
    university="KBTU"
)
