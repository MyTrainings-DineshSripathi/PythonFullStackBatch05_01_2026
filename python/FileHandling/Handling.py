# file = open('C:\\Users\\Dell\\Downloads\\GitRepos\\PythonFullStackBatch05_01_2026\\python\\FileHandling\\Files\\file1.txt', 'r')

# # file.write("Hello this content was placed in python code 1")



# content = file.read()
# print(content)

# file.close()

import OOP.Car


with open('C:\\Users\\Dell\\Downloads\\GitRepos\\PythonFullStackBatch05_01_2026\\python\\FileHandling\\Files\\file1.txt', 'r') as f:
    fileContent = f.read()
    print(fileContent)