# class Car:    
#     def __init__(self, name="", model="", make="", year=0 ):
#         self.__name = name
#         self.model = model
#         self.make = make
#         self.year = year
#         print(self,"Object created")
        
#     def setName(self, name):
#         self.__name = name
    
#     def getName(self):
#         return self.__name
        
#     def start(self):
#         print(f"{self.__name} started...")
    
#     def stop(self):
#         print(f"{self.__name} stopped...")
        
#     def __str__(self):
#         return f"name = {self.__name}, model = {self.model}, make = {self.make}, year={self.year}"
    

# class Truck(Car):
#     def truckProp(self):
#         print("This is a truck property")
        

# class Sample(Car):
#     pass

# s1 = Sample()

# s1.start()
# s1.truckProp()

# car1 = Car()
# car2 = Car()

# # car1.__name = "Maruthi"
# car1.setName("Maruthi")
# # print(car1.name)
# # car1.__name = "Audi"
# car1.setName("Audi")
# # car2.__name = "BMW"
# car2.setName("BMW")

# print(car1.getName())
# print(car2.getName())

# car3 = Car(name="Benz", model="B123", make="Benz Lux", year=2000)

# # print(car3.name)

# print(car1)
# print(car2)
# print(car3)

# car1.start()
# car2.start()

# car1.stop()
# car2.stop()

# # object creation of truck class
# t1 = Truck()

# t1.setName("Ashok Leyland")
# t1.model = "AL2"
# t1.make= "Heavy Vehicle"
# t1.start()
# t1.stop()

from abc import ABC, abstractmethod

class Payment(ABC):
    __amount = 0
    
    def setAmount(self,amount):
        self.__amount = amount
        
    def getAmount(self):
        return self.__amount
    
    @abstractmethod
    def pay(self):
        pass
    
# p1 = Payment()

# p1.pay()

class OnlinePayment(Payment):
    def pay(self):
        print("Scanning QR code")
        print("fetched bank details")
        print("payment processing")
        print(self.getAmount(),' is payed')

class cashPayment(Payment):
    def pay(self):
        print(self.getAmount(),' is payed')

p1 = cashPayment()
p1.setAmount(3000)
p1.pay()