class Test:
    def __init__(self):
        self.name = ''
        self.age = 0
    
    def displayInfo(self):
        print(f"User name : {self.name} and age : {self.age}")
    
class Dummy(Test):
    pass
        
test1 = Dummy()

test1.name = "Tony Stark"
test1.age = 40

test1.displayInfo()