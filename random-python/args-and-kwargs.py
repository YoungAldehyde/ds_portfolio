#*args = arguments
#**kwargs = keyword arguments
#allows python function to accept unspecified/arbitrary amount of arguments and keyword arguments

#
def print_args(*args):
    print(f"These are my arguments : {args}")

print_args([1,2,3], (8,9), {'key': 4 })

#
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

print_kwargs(x = "hello", y = "test")

#
def add(*args):
    my_sum = 0
    for arg in args:
       try:
        arg = int(arg)
        my_sum += arg
       except ValueError:
            continue
    return my_sum


add(3, 4)

add(3, 5, 7)

def outer_function(func):
    def inner_func(*args, **kwargs):
        print(f"Our inner_func is {func.__name__}") #python 3.6+ only
        return func(*args, **kwargs)
    return inner_func

@outer_function
def add(num1, num2):
    return num1 + num2

@outer_function
def print_name(name):
    print(f"hello there {name}")

add(3, 4)

print_name("Hi Im Hungry")


#
class SuperClass():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MySubclass(SuperClass):
    def __init__(self, z ,*args, **kwargs): # order is z first and *args, **kwargs
        self.z = z
        super().__init__(*args, **kwargs)


test = SuperClass(2,3)

print(test.x, test.y)

test2 = MySubclass(1,8,9)


test2.x, test2.y ,test2.z