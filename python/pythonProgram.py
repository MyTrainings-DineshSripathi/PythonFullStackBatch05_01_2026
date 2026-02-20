# userAge = 45

# UserAge = 39

""" 
    operations : 
        1. assignment
        2. math -- +, -, /, %, *, **
        3. comp -- >, <, ==, !=, >=, <= 
        4. logical - and or not
            and : 2 inputs -- false --> result -false
            
            input1  input2  output
            true    true    true
            true    false   false
            false   true    false
            false   false   false
            
            or : 2 inputs -- true --> result : true
            
            input1  input2 output
            true    true    true
            true    false   true
            false   true    true
            false   false   false
            
            not : 1 input   --- Result : opp
            
            input   output
            true    false
            false   true
        5. bitwise     
            & | ~ ^ << >>
            
               
"""

# print(userAge)
# print(UserAge)

# print(6 + 5)
# print(6 / 5)
# print(6 % 5)
# print(6 ** 3)
# print(6 + 9 - 5 / 2 * 3 + (3 - 5 * 2))#17.3
# BODMAS 

# value1 = 5
# value2 = 6

# value3 = value1 + value2

# # add value1 with value2 and store the result in value1

# # value1 = value1 + value2
# value1 += value2

# print(value1)

# database data fetched by using email
# database_email = "ravi@gmail.com"
# database_username = "Ravi_Kumar"
# database_password = "Ravi@1234"

# # frontend request data
# frontend_userEmail = "ravi@gmail.com"
# frontend_username = "Ravi_Kishore"
# frontend_userPassword = "Ravi@1234"

# filter option
# frontend_filter_salary = 300000

# database_salary = 300000


# we can allow user if email or username is correct and password as well

# print(database_email == frontend_userEmail and database_password == frontend_userPassword or database_username == frontend_username)


# print(database_salary >= frontend_filter_salary)
# print(5 >> 3) 

# print(5 | 77)
# print(86 ^ 77)

# print(~5)
# print(~ -7)

# print(10 << 2)
# print(10 >> 2)

# statements 

""" 
indendation : 

control statements
    1. condition statements: 
        setting a rule for a set of statements or a statement to get executed.
        if/ simple if : 
            considers a condition and if the condition is true then executes the statement or else it will skip the statement inside the if block.
            
            syntax : 
                if condition:
                    block of statements
        if else
            syntax : 
                if condition :
                    block of if 
                else:
                    block of else
        if elif
            syntax : 
                if condition : 
                    block of if
                elif condition1:
                    block of elif1
                .
                .
                .
                else:
                    block of else
        match
            syntax : 
                match(input):
                    case value:
                        block of case
                    .
                    .
                    .
        nested conditional statements
    2. iterative statements : 
        for
            syntax : 
                for variable in range():
                    block
        while
            syntax : 
                variable = starting
                
                while(condition):
                    block of code
                    variable update
"""


# if False:
#     print("Statement of If block1")
#     print("Statement of If block2")
#     print("Statement of If block3")
#     print("Statement of If block4")
#     print("Statement of If block5")


# isAllFieldsFilled = True

# if isAllFieldsFilled:
#     print("he is ok to move forward")
# else:
#     print("he is not ok to move forward")
    
""" 
    Grade assignment : 
        - 90 -- O Grade
        - 70 - 90 -- A Grade
        - 50 - 70 -- B Grade
        - 30 - 50 -- C Grade
        - 30 - Fail
"""
# marks = 80

# if marks >= 90:
#     print("O Grade")
# elif marks >= 70:
#     print("A Grade")
# elif marks >= 50:
#     print("B Grade")
# elif marks >= 30:
#     print("C Grade")
# else:
#     print("Fail")

# value = 3

# match(value):
#     case 1:
#         print("case 1")
#     case 3:
#         print("case 3")
#     case 2:
#         print("case 2")

# for var in range(1, 101):
#     print(var,"My Statement")
    
# var = 1

# while(var <= 100):
#     print(var,"My Statement")
#     var += 1

""" 
    take 3 values and find the largest number b/w 3 values.
    3,5,4
    
    - 5 
    
    taken : 3  taken > 5 and taken > 4 -- 3
    taken : 5  taken > 3 and taken > 4 -- 5
    taken : 3  taken > 5 and taken > 4 -- 4
    
    a = 4
    b = 3
    c = 5
    
    if(a > b and a > c):
        print(a, "is bigger than",b,c)
    elif(b > a and b > c):
        print(b, "is bigger than",a,c)
    else:
        print(c, "is bigger than",b,a)
        
    find wheather the given number is a positive or negative number.
    
    < 0 -- negative
    >= 0 -- positive
    
    value = int(input("Enter a value : "))
    
    if(value < 0):
        print("Negative number")
    else:
        print("Positive number")
    
    find wheather the given number is a even or odd number
    number%2 == 0
"""

# a = int(input("Enter 1st value : "))
# b = int(input("Enter 2nd value : "))
# c = int(input("Enter 3rd value : "))

# if(a > b and a > c):
#     print(a, "is bigger than",b,c)
# elif(b > a and b > c):
#     print(b, "is bigger than",a,c)
# else:
#     print(c, "is bigger than",b,a)

# value = int(input("Enter a value : "))
    
# if(value < 0):
#     print("Negative number")
# else:
#     print("Positive number")

# number = int(input("Enter a value to check if it is a even or not"))

# if(number%2 == 0):
#     print(number,"is even number")
# else:
#     print(number,"is odd number")
""" 
    break
    pass
    continue
"""

# for i in range(1, 11):
#     if(i == 4 or i == 5 or i == 7):
#         continue
#     print(i)

# if True:
#     pass

""" 
    function : Reusable block of code.
    
    syntax : 
        def functionName(parameters(optional)):
            block of code
"""



# def sampleFunction():
#     print("A single line of code 1")
#     print("A single line of code 2")
#     print("A single line of code 3")
#     print("A single line of code 4")
#     print("A single line of code 5")


# sampleFunction()

# print("another set of code")
# print("another set of code")

# print("A single line of code 1")
# print("A single line of code 2")
# print("A single line of code 3")
# print("A single line of code 4")
# print("A single line of code 5")

# sampleFunction()

# print("lorem contnent here and there there is nothing")

# sampleFunction()
# print("A single line of code 1")
# print("A single line of code 2")
# print("A single line of code 3")
# print("A single line of code 4")
# print("A single line of code 5")

# def isEvenOrOdd(number):
#     if(number%2 == 0):
#         print(number, "is even number.")
#     else:
#         print(number,"is odd number.")


# isEvenOrOdd(3)    
    
# print("A single line of code 1")
# print("A single line of code 2")
# print("A single line of code 3")
# print("A single line of code 4")
# print("A single line of code 5")

""" 
1. write a program to check if a given number is prime number or not
2. write a function to reuse prime number logic 
3. convert all the assignments to functions.
"""

# number = 23

# zeroCounter = 0

# num = number//2

# for i in range(1, num + 1):
#     if(number % i == 0):
#         zeroCounter += 1

# if(zeroCounter == 1):
#     print(number,"is a prime number")


""" 
    list : collection of data - []
        - we use index values to access the data individully
            -   start -- 0
            -   end   -- (list-length - 1) //total no.of values stored inside the list.
        - duplicates, changable, ordered
"""

# reels = [1,2,3,4,5]
# posts = [11,12,13]

# reels[4] = 55

# # insert - inserts data to the given index
# reels.insert(5, 6)
# # append - adds the data at the end of the list
# reels.append(7)
# # extend - adds the other collection data as seperate elements to the list
# reels.extend(posts)

# # pop - using index or removing last element
# reels.pop()
# reels.pop(2)
# # remove - removes the specified element
# reels.remove(11)

# reels.append(12)

# for value in reels:
#     print(value)

# print("size of list : ",len(reels))

# evenList = []

# for value in reels:
#     if value % 2 == 0:
#         evenList.append(value)
        
# """ 
#     compreh : 
#         syntax : 
#             [value loop condition]
# """

# compEvenList = [value for value in reels if value%2==0]

# print("even list : ",evenList)
# print("even list comp : ",compEvenList)
# print("before sorting ; ",reels)
# reels.sort(reverse=True)
# print("after sorting : ",reels)

# """ 
#     list -- 101
#     reels -- 101
#     b = reels // 101
# """

# b = reels.copy()
# # b = [x for x in reels]
# print(reels)
# print("b : ", b)
# b.append(100)
# print("reels",reels)
# print("b : ", b)

""" 
    tuple : collects the data --> ()
        - allows duplicate, ordered, not change values
        - can access data using index values
        - can only access the data.
"""

# listData = [1,2,3,4,5,6,7]

# sample = tuple(listData)

# # sample[0] = 11

# # index -- finds the index for the given value
# print(sample.index(3))
# print(sample[3])

# print(len(sample))

# print(sample)

# for i in sample:
#     print(i)

""" 
    set : collects the data --> {}
        -- will not allow duplicates, unordered
        -- can't use index values to access data
        -- we can add data, remove
"""

# sample = {1,12,13,4,5,11,2,3}

# sample_subset = {12,13,4,5}

# test = {1,2,3,4,21,22,23,24}

# sample.add(34)
# sample.remove(3)
# # sample.clear()

# result = sample.union(test)
# print("result : ",result)

# result = sample.intersection(test)
# print("result : ",result)

# result = sample.difference(test)
# print("result : ",result)

# result = sample.isdisjoint(test)
# print("result : ",result)

# result = sample.issuperset(sample_subset)
# print("result : ",result)

# result = sample.issubset(sample_subset)
# print("result : ",result)

# sample.difference_update(test)



# print("sample",sample)

# for i in sample:
#     print(i)

""" 
    dict : 
        -- will store data in key pair values -- {}
        -- ordered, allows duplicate data but not duplicate key
        -- It will not have index value to access the data.
        
"""

# sample = {
#     "name" : "Dinesh",
#     "age" : 189,
#     "phone" : 9987654667,
#     "age" : 12,
#     "email" : "dinesh@gmail.com"
# }

# print(sample)
# print(sample.get("name"))
# print(sample["name"])

# # sample["name"] = "Tony"
# sample.update({"name" : "Tony Stark"})

# print(sample)

# print(sample.keys())
# print(sample.values())
# print(sample.items())

# for i in sample.keys():
#     print(sample.get(i))
    
# for (i, j) in sample.items():
#     print(i,j)

""" 
    strings : collection of characters
"""

# name = " tony stark "
# print(name)

# print(name[0])

# name[0] = 'Z'

# print(name)

# for i in name:
#     print(i)
    
""" 
    in
        -- checks if given character is available inside the collection or not
    is
        --compares if the given character is equal to other character
"""

# if "y" in name:
#     print("Stark present in the name")
# else:
#     print("not present")

# print(name.capitalize())
# print(name.upper())
# print(name.lower())
# print(name.strip())
# print(name.lstrip())
# print(name.rstrip())
# print(name.isupper())
# print(name.islower())
# print(len(name))
# print(name.replace("n","i"))
# print(name.endswith("."))
# print(name.startswith("t"))
# print(name.swapcase())
# print(name.split("t"))
# dividedList = name.split(' ')
# print(dividedList)
# print(''.join(dividedList))

# print(name[6 : ])
# print(name[-2])
# print(name[-8:-2])
# print(name[0::1])
# print(name[::-1])

# sentance = f"Iron man is {name}"

# print(sentance)


""" 
    project : 
        data1 
        data2
        data3
        .
        .
        .
        data10
        
        data11
    OOP in python : 
        1. Class : 
            blue print of an object.
            
            syntax : 
                class classname:
                    //properties
        2. Object : 
            instance of a class. This helps us to store data related to class.
            
            syntax : 
                objName = classname()
        3. Encapsulation
        4. inheritance
        5. abstraction

"""

from OOP import Car as c

car1 = c.OnlinePayment()

print(car1)
