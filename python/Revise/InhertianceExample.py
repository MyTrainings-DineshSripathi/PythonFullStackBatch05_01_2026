class UsersRegistration:
    def saveUserDetails(self):
        print(f"Saved {self.fullname} details")

#ABC Abstract Base Class -- it coverts a normal class to abstract class
# we can only use abstract methods inside abstract class --> we have to inherit ABC to class
#  to declare abstract methods we use @abstract decorator

from abc import ABC, abstractmethod

class Payments(ABC):
    @abstractmethod
    def pay(self):
        pass
# amazon -- seller, consumer
# seller -- gst reg, business name, products
# consumer -- orders

class UPI(Payments):
    def pay(self):
        print("UPI Payment completed")

class CreditCard(Payments):
    def pay(self):
        print("Credit card payment recieved")

class Seller(UsersRegistration):
    def __init__(self,fullname, email, phone, password, date, address, gstReg, businessName, products):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.password = password
        self.joiningDate = date
        self.address = address
        self.gstReg = gstReg
        self.businessName = businessName
        self.products = products 

class Consumer(UsersRegistration, CreditCard):
    def __init__(self,fullname, email, phone, password, date, address,orders):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.password = password
        self.joiningDate = date
        self.address = address
        self.orders = orders

consumer1 = Consumer("Krishna Kumar", "krishna@email.com", 9876543341, "Krishna@1234", "09/12/2025", "Kukatpally, Hyderabad, 500082", ['Apple 15 pro', 'PSP5'])


seller1 = Seller("Ravi Kumar", "ravi@email.com", 9876543341, "Ravi@1234", "09/11/2023", "KPHB, Hyderabad, 500085", "GST09867556561A", "Smart Groming", ['Trimmer', 'neem comb', 'eye brow pencil'])

seller1.saveUserDetails()
consumer1.saveUserDetails()

consumer1.pay() #upi/ online

print(seller1.fullname)
print(seller1.businessName)

