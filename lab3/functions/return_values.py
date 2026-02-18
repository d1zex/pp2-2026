# This function calculates something and RETURNS the result.
# Returning is different from printing.
# When we return, we can store the result in a variable.

def add_numbers(a, b):
    result = a + b
    return result  # send result back to where the function was called

# Store the returned value in a variable
sum_result = add_numbers(5, 7)

print("Poluchaetsya:", sum_result)