from functools import wraps

# Custom decorator
def my_decorator(func):
    @wraps(func)  # Use @wraps to preserve metadata
    def wrapper(*args, **kwargs):
        print("Before the function is called")
        result = func(*args, **kwargs)
        print("After the function is called")
        return result
    return wrapper

# Applying the decorator to a function
@my_decorator
def my_function():
    """This is the docstring of my_function."""
    print("Inside my_function")

# Accessing metadata of the decorated function
print(my_function.__name__)  # Output: "my_function"
print(my_function.__doc__)   # Output: "This is the docstring of my_function."

my_function()

