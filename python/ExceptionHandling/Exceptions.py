print("line 1")
print("line 1")
print("line 1")
print("line 1")

class CustomException(Exception):
    ...

try:
    a = 2
    b = 0
    
    if(b > 0):
        print(a/b)
    else:
        raise CustomException("Here we got an error in custom Exception")
except (ArithmeticError, CustomException) as e:
    print(e)

print("line 1")
print("line 1")
print("line 1")
print("line 1")
print("line 1")
print("line 1")

