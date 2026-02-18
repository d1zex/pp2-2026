# Lambda is a small anonymous (nameless) function.
# It is useful when we need a simple function for a short time.

# Normal function version
def square(x):
    return x * x

print("Normal function result:", square(5))


# Lambda version (shorter)
# Syntax: lambda arguments : expression
square_lambda = lambda x: x * x

print("Lambda function result:", square_lambda(5))


# We can even use lambda directly without saving it
print("Direct lambda result:", (lambda x: x * x)(6))
