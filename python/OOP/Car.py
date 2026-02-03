class Car:    
    def __init__(self, name="", model="", make="", year=0 ):
        self.name = name
        self.model = model
        self.make = make
        self.year = year
        print(self,"Object created")
    
    def __str__(self):
        return f"name = {self.name}, model = {self.model}, make = {self.make}, year={self.year}"
    

car1 = Car()
car2 = Car()

car1.name = "Maruthi"
# print(car1.name)
car1.name = "Audi"
car2.name = "BMW"

# print(car1.name)
# print(car2.name)

car3 = Car(name="Benz", model="B123", make="Benz Lux", year=2000)

# print(car3.name)

print(car1)
print(car2)
print(car3)