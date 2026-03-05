class BikeRegistration:
    # brand = ''
    # features = ''
    # fuelType = ''
    # lanchYear = ''
    # life = ''
    # registrationNo = ''
    
    def __init__(self, brand='', features='', fuelType='', launchYear='', life='', registrationNo=''):
        print("object created", self)
        self.brand = brand
        self.features = features
        self.fuelType = fuelType
        self.launchYear = launchYear
        self.life = life
        self.registrationNo = registrationNo
        
    def display(self):
        return f"Displaying Bike Details \n ---------------------- \n Bike Brand = {self.brand}, Features = {self.features}, Launch Year = {self.launchYear}, Fuel Type = {self.fuelType}, Life = {self.life}, Registration no = {self.registrationNo}"
    
bike1 = BikeRegistration()

bike2 = BikeRegistration("Honda", "led headlight, led taillight, speedometer, usb charging", "petrol", 2025, 29, "TG09T2345" )



bike1.brand = "Hero"
bike1.features = "led headlight, led taillight, speedometer, usb charging"
bike1.fuelType = "petrol"
bike1.lanchYear = 2024
bike1.life = 28
bike1.registrationNo = "TG07GH1234"

print(bike1.brand, bike1.features)
print(bike2.brand, bike2.features)


print(bike1.display())
print(bike2.display())