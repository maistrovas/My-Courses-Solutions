'''
Problem_1

1.Suppose x = "me" and y = "myself". The lines
of code x = y and then y = x will swap the 
values of x and y, resulting in x = "myself" and y = "me".
-False

2.Suppose x is an integer in the following code:
def f(x):
    while x > 3:
        f(x+1)
For any value of x, all calls to f are guaranteed to never terminate.
-False

3.A Python program may execute a line of code more than once.
-True

4.In Python, a list can be aliased.
-True

5.The following code will enter an infinite loop for all values of i and j.
while i >= 0:
    while j >= 0:
        print i, j
-False

6.A Python dictionary is a mutable object.
 -True

7.It is always possible and feasible for a programmer 
to come up with test cases that run through every possible 
path in a program.
-False

8.A program that contains the line x = 3'a' is syntactically incorrect.
-True

9.Consider the following function.
def f(x):
    a = []
    while x > 0:
        a.append(x)
        f(x-1)
A new object of type list is created for each 
recursive invocation of f.
-True

10.Any number that can be represented as a decimal fraction can be 
represented exactly in floating point representation in Python.
-False
'''



'''
Problem_2

1.Consider the statement:
 L = {'1':1, '2':2, '3':3}. Which is correct?
-L maps strings to integers

2.Which of the following is true?
- Testing compares program output to 
the expected output. Debugging is a 
process to study the events leading 
up to an error.

3.In Python, which of the following 
can be aliased in a way that affects 
the behavior of the program?
-a list a list

4.Assume a break statement is executed 
inside a loop and that the loop is inside 
a function. Which of the following is correct?
---------Not Answer

5.Choose the item from the list of potential 
responses that best matches: [:]
-cloning
'''



'''
Problem_3

1.Examine the following code snippet:

  stuff  = _____
  for thing in stuff:
        if thing == 'iQ':
           print "Found it"
Select all the values of the variable 
"stuff" that will make the code print "Found it".
-["iBoy", "iGirl", "iQ", "iC","iPaid","iPad"]
-("iBoy", "iGirl", "iQ", "iC","iPaid","iPad")
-["iQ"]

2.The following Python code is supposed to compute 
the square of an integer by using successive additions.
def Square(x):
    return SquareHelper(abs(x), abs(x))

def SquareHelper(n, x):
    if n == 0:
        return 0
    return SquareHelper(n-1, x) + x
Not considering recursion depth limitations, 
what is the wrong with this implementation of 
procedure Square? Check all that apply.
-Nothing is wrong; the code is fine as-is.
'''



'''
Problem_4

Write a Python function, evalQuadratic(a, b, c, x), 
that returns the value of the quadratic a⋅x2+b⋅x+c.

This function takes in four numbers and returns a single number.
'''
def evalQuadratic(a, b, c, x):
    '''
    a, b, c: numerical values for the coefficients of a quadratic equation
    x: numerical value at which to evaluate the quadratic.
    '''
    return (a*(x**2))+ (b*x)+c

def twoQuadratics(a1, b1, c1, x1, a2, b2, c2, x2):
    '''
    a1, b1, c1: one set of coefficients of a quadratic equation
    a2, b2, c2: another set of coefficients of a quadratic equation
    x1, x2: values at which to evaluate the quadratics
    '''
    x = evalQuadratic(a1, b1, c1, x1)
    y = evalQuadratic(a2, b2, c2, x2)
    
    print (x+y)
'''
Problem_5

Write a Python function that creates and returns a list of 
prime numbers between 2 and N, inclusive, sorted in 
increasing order. A prime number is a number that is 
divisible only by 1 and itself. This function takes in an 
integer and returns a list of integers.

'''
def primesList(N):
    '''
    N: an integer
    '''
    liss = []
    for i in range(2, N+1):
        prime = True
        for j in range(2, i-1):
            if i % j == 0:   
                prime = False
                pass
        if prime:
            liss.append(i)
    return liss



'''
Problem_6

Write a recursive Python function, given a non-negative 
integer N, to count and return the number of occurrences 
of the digit 7 in N.
'''
count  = 0 
def count7(N):
    global count
    '''
    N: a non-negative integer
    '''
    if N % 10 == 7:
        count +=1
    if N == 0:
        count1 = count 
        count = 0
        return count1
    else:
        return count7(N/10)


'''
Problem_7

Write a Python function that returns a list of keys in aDict 
that map to integer values that are unique (i.e. values appear 
exactly once in aDict). The list of keys you return should 
be sorted in increasing order. (If aDict does not contain any 
unique values, you should return an empty list.)
This function takes in a dictionary and returns a list.
'''
def uniqueValues(aDict):
    '''
    aDict: a dictionary
    '''
    # Your code here
    uniq = []
    vals = [aDict[x] for x in aDict]
    for key in aDict:
        clone = vals[:]
        clone.remove(aDict[key])
        if aDict[key] not in clone:
            uniq.append(key)
    return uniq

#diction = {1: 1, 2: 1, 3: 1}
#print uniqueValues(diction)
'''
Problem_8

Write a Python function called satisfiesF that has the 
specification below. Then make the function call 
run_satisfiesF(L, satisfiesF). Your code should look like:
'''
def f(s):
    return 'a' in s

def satisfiesF(L):
    '''
    L - a list of strings
    Assume function f is already defined for you and it maps a string to a Boolean
    Mutates L such that it contains all of the strings, s, originally in L such
            that f(s) returns True, and no other elements
    Returns the length of L after mutation
    '''
    for string in L[:]:
        if not f(string):
            L.remove(string)
    return len(L)

# L = ['a', 'b', 'a']
# print satisfiesF(L)
# print L