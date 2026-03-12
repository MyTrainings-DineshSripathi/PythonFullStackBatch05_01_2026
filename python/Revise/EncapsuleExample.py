class Book:
    __author = ''
    __title = ''
    price = ''
    def setAuthor(self, author):
        self.__author = author
    def getAuthor(self):
        return self.__author
    
class Publisher(Book):
    name = ''
    address = ''
    def __init__(self):
        super().__init__()
    
    def publishBook(self):
        print(f"{self.title} is a book written by {self.author}. published with price {self.price} by {self.name}")
        

book1 = Book()

book1.setAuthor("Rajiv")
book1.author = "Rajiv"
book1.title = "My Life as a sailor"
book1.price = 300


publisher = Publisher()

publisher.name = "KVV publishers"
publisher.address = "KPHB, Hyderabad 500085"
publisher.title = book1.title
publisher.price = book1.price

publisher.publishBook()