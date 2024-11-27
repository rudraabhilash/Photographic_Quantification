'''
other programming languages
int answer = 56;
String name = "Rahul";
'''

#python syntax
answer = 56
name = "Rahul"

'''
def AreaOfRectangle():
    length = 5 # Variable declared locally
    breadth = 6 # Variable declared locally 
    print("length = {} and breadth = {}".format(length,breadth)) # Calling local variable inside function
    return length * breadth

print(AreaOfRectangle()) #Calling the function to print result
'''


'''
def AreaOfRectangle():
    length = 5 # Variable declared locally 
    breadth = 6 # Variable declared locally 
    return length * breadth

print("length = {}".format(length)) # Calling local Variable outside function
'''


'''
length = 5 # declaring length out of function
breadth = 6 # declaring breadth out of function

def AreaOfRectangle():
    print("length = {} and breadth = {}".format(length,breadth)) # Calling local variable inside function
    return length * breadth

print("length = {}".format(length + 2)) # Calling the variable length outside function and increasing the length value.
print(AreaOfRectangle()) #Calling the function to print result
'''

'''
length = 5 # declaring length out of function
breadth = 6 # declaring breadth out of function

def AreaOfRectangle():
    length += 2   #length = length + 2
    print("length = {} and breadth = {}".format(length,breadth)) # Calling local variable inside function
    return length * breadth

print(AreaOfRectangle()) #Calling the function to print result
'''


'''
length = 5 # declaring length out of function
breadth = 6 # declaring breadth out of function

def AreaOfRectangle():
    global length # defining local variable to global variable
    length += 2
    print("length = {} and breadth = {}".format(length,breadth)) # Calling local variable inside function
    return length*breadth

print(AreaOfRectangle()) #Calling the function to print result
'''
'''
x=10
print( float(x) )
'''

'''
x=10
if x == 10:
    print("I am inside if block!")
else:
    print("I am inside else block!")
'''    

'''
x=5
while x>0:
    print(x)
    x-=1
'''

'''
x=5
while x>0:
    print(x)
    x-=1
    if x == 3:
        break
'''

'''
x=5
while x>0:
    x-=1
    if x == 2:
        continue
    print(x)
'''


'''
Fruits = ["Lemon", "Apple", "Orange", "Strawberry"] #accessing items of the list using for loop
for fruit in Fruits:
      print(fruit)
'''

'''
numbers = [10,20,30,40,50,60,70,80,90,100]
for num in numbers:
     if num == 60: #print number 10 to 50 , terminate loop at number 60
        break
     print(num)
'''

#Lists
'''
squares = [1, 4, 9, 16, 25]
print(squares)
print(squares[0])
print(squares[-1])
print(squares[-3:])  # slicing returns a new list
print(squares + [36, 49, 64, 81, 100])
squares[4] = 36 #change existing element 
squares.append(216)
print(squares)

list = ['larry', 'curly', 'moe']
list.append('shemp')         ## append elem at end
list.insert(0, 'xxx')        ## insert elem at index 0
list.extend(['yyy', 'zzz'])  ## add list of elems at end
print(list)  ## ['xxx', 'larry', 'curly', 'moe', 'shemp', 'yyy', 'zzz']
print(list.index('curly'))    ## 2

list.remove('curly')         ## search and remove that element
list.pop(1)                  ## removes and returns 'larry'
print(list)  ## ['xxx', 'moe', 'shemp', 'yyy', 'zzz']

list = [1, 2, 3]
print(list.append(4))   ## NO, does not work, append() returns None
## Correct pattern:
list.append(4)
print(list)  ## [1, 2, 3, 4]
letters = ['a', 'b', 'c', 'd']
print(len(letters))
'''

#Tuple
'''
t = 12345, 54321, 'hello!'
print(t)

# Tuples may be nested:
u = t, (1, 2, 3, 4, 5)
print(u)

# Tuples are immutable:
t[0] = 88888


# tuple can contain mutable objects:
v = ([1, 2, 3], [3, 2, 1])
print(v)
'''

#set
'''
set_fruit = {"apple", "cherry", "banana", "cherry"}

for fruit in set_fruit:
  print(fruit)
'''


#dictionary
'''
car_dict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020,
  "colors": ["red", "white", "blue"]
}
print(car_dict)
print(car_dict["brand"])
print(len(car_dict))
print(type(car_dict))
'''
