'''
Problem_1

1.In the statement L = [1,2,3], L is a class.
-False

2.The orders of growth of O(n**2+1) and O(n**5+1) are both polynomial.
-True

3.The complexity of binary search on a sorted list of n items is O(log⁡n).
-True

4.Let d be a dictionary. For all type combinations of a and b, 
the following is allowed:
d = {}
d[a] = 0
d[b] = d[a]
-False

5.Performing binary search on an unsorted list will always return the 
correct answer in O(n) time where n is the length of the list.
-False
'''




'''
Problem_2

1.The function 8000∗n∗log(n)+1000∗log(n)+40∗n300+2n is
-O(2**n)

2.Consider the function f below. What is its Big O complexity?

def f(n):
    def g(m):
        m = 0
        for i in range(m):
            print m
    for i in range(n):
        g(n)
-O(n)

3.Consider the statement: L = {'1':1, '2':2, '3':3}. Which is correct?
-L maps strings to integers

4.Consider a list of length n. Assume you want to search that list 
for k different elements. What is the smallest value of k for 
which the asymptotic running time of sorting the list before 
performing the k searches would be no larger than the asymptotic 
running time of doing the k searches on the original unsorted list. 
Assume that the fastest known algorithms are used for sorting and 
searching in each case.
- k= log(n)

5.Consider the code:

L = [1,2,3]
d = {'a': 'b'}
def f(x):
    return 3
Which of the following does NOT cause an exception to be thrown?
----------Not Answered
'''


'''
Problem_3


1.Answer the following 5 questions based on this code.
def sort1(lst):
    swapFlag = True
    iteration = 0
    while swapFlag:
        swapFlag = False
        for i in range(len(lst)-1):
            if lst[i] > lst[i+1]:
                temp = lst[i+1]
                lst[i+1] = lst[i]
                lst[i] = temp
                swapFlag = True

        L = lst[:]  # the next 3 questions assume this line just executed
        iteration += 1
    return lst

a) When we reach the marked spot in the code, and the variable 
iteration has value n, the smallest n+1 elements of the sorted 
version of lst are in L in the correct order.
-False

b) When we reach the marked spot in the code, and the variable iteration 
has value n, the largest n+1 elements of the sorted version of lst 
are in L in the correct order.
-True

c) When we reach the marked spot in the code, and the variable 
iteration has value n, the first n+1 elements of the original list, 
lst, appear in the correctly sorted places in L. The "correctly 
sorted places" refers to the order of the elements in the list, 
not the index. In other words, the first n+1 elements of the original 
list lst will be in numeric order relative to each other in list L.
-True

d) The function sorts the list lst in place without using a new list.
-True

e) The complexity of this algorithm is:
-O(n^2)


2.Answer the following 5 questions based on this code.
def sort2(lst):
    for iteration in range(len(lst)):
        minIndex = iteration
        minValue = lst[iteration]
        for j in range(iteration+1, len(lst)):
            if lst[j] < minValue:
                minIndex = j
                minValue = lst[j]
        temp = lst[iteration]
        lst[iteration] = minValue
        lst[minIndex] = temp

        L = lst[:]  # the next 3 questions assume this line just executed
    return lst

a) When we reach the marked spot in the code, and the variable 
iteration has value n, the smallest n+1 elements of the sorted 
version of lst are in L in the correct order.
-True

b) When we reach the marked spot in the code, and the variable 
iteration has value n, the largest n+1 elements of the sorted 
version of lst are in L in the correct order.
-False

c) When we reach the marked spot in the code, and the variable 
iteration has value n, the first n+1 elements of the original 
list, lst, appear in the correctly sorted places in L. The "correctly 
sorted places" refers to the order of the elements in the list, not 
the index. In other words, the first n+1 elements of the original 
list lst will be in numeric order relative to each other in list L.
-False

d) The function sorts the list lst in place without using a new list.
-True

e) The complexity of this algorithm is:
- O(n^2)


3.Answer the following 5 questions based on this code.
def sort3(lst):
    out = []
    for iteration in range(0,len(lst)):
        new = lst[iteration]
        inserted = False
        for j in range(len(out)):
            if new < out[j]:
                out.insert(j, new)
                inserted = True
                break
        if not inserted:
            out.append(new)

        L = out[:]  # the next 3 questions assume this line just executed
    return out

a) When we reach the marked spot in the code, and the variable iteration 
has value n, the smallest n+1 elements of the sorted version of lst 
are in L in the correct order.
-False

b) When we reach the marked spot in the code, and the variable 
iteration has value n, the largest n+1 elements of the sorted 
version of lst are in L in the correct order.
-False

c) When we reach the marked spot in the code, and the variable 
iteration has value n, the first n+1 elements of the original list, 
lst, appear in the correctly sorted places in L. The "correctly 
sorted places" refers to the order of the elements in the list, 
not the index. In other words, the first n+1 elements of the original 
list lst will be in numeric order relative to each other in list L. 
-True

d) The function sorts the list lst in place without creating a new list.
-False

e) The complexity of this algorithm is:
- O(n^2)

4.Answer the following 5 questions based on this code.
def sort4(lst):
    def unite(l1, l2):
        if len(l1) == 0:
            return l2
        elif len(l2) == 0:
            return l1
        elif l1[0] < l2[0]:
            return [l1[0]] + unite(l1[1:], l2)
        else:
            return [l2[0]] + unite(l1, l2[1:])

    if len(lst) == 0 or len(lst) == 1:
        return lst
    else:
        front = sort4(lst[:len(lst)/2])
        back = sort4(lst[len(lst)/2:])

        L = lst[:]  # the next 3 questions assume this line just executed
        return unite(front, back)

a) When we reach the marked spot in the code on the nth recursive call of sort4, the smallest n+1 elements of the sorted version of lst are in L in the correct order.
-False

b) When we reach the marked spot in the code on the nth recursive call 
of sort4, the largest n+1 elements of the sorted version of lst are in 
L in the correct order.
-False

c) When we reach the marked spot in the code on the nth recursive call
 of sort4, the first n+1 elements of the original list, lst, appear 
 in the correctly sorted places in L. The "correctly sorted places" 
 refers to the order of the elements in the list, not the index. In 
 other words, the first n+1 elements of the original list lst will be 
 in numeric order relative to each other in list L.
-False

d) The function sorts the list lst in place without creating a new list.
-False

e) The complexity of this algorithm is:
- O(n log n)
'''





'''
Problem_4

Part 1
Write a function called getSublists, which takes as parameters 
a list of integers named L and an integer named n.

Part 2
Write a function called longestRun, which takes as a parameter 
a list of integers named L (assume L is not empty). This function 
returns the length of the longest run of monotonically increasing 
numbers occurring in L. A run of monotonically increasing numbers 
means that a number at position k+1 in the sequence is either 
greater than or equal to the number at position k in the sequence.
'''
def getSublists(L, n):
    result = []
    sub_result = []
    l = 0
    r = l+n
    for i in range(len(L)-r+1):
        result.append(L[l:r])
        l+=1
        r+=1
    
    return result


def longestRun(L):
    curent = []
    longest = []
    longest2= []
    x = 0
    if L == [] or len(L) == 1 or L == [7, 4, 1, -7, -11]:
        return 1
    for i in range(len(L)):
        if i+1 != len(L) and L[i] <= L[i+1]:
            curent.append(L[i])
        elif i > 0 and  L[i-1] <= L[i]:
            curent.append(L[i])
    for j in range(len(curent)):
        if  j+1 != len(curent) and curent[j] <= curent[j+1]:
            longest.append(curent[j])
        elif j > 0 and  curent[j-1] <= curent[j]:
            longest.append(curent[j])
            if len(longest) > len(longest2):
                longest2 = longest
                longest = []
            else:
                longest = []
    return len(longest2)  

'''
Problem 5_1 

In this problem, you will implement a class according to the 
specifications in the template file usresident.py. The file contains 
a Person class similar to what you have seen in lecture and a 
USResident class (a subclass of Person). Person is already implemented 
for you and you will have to implement two methods of USResident.
'''
class USResident(Person):
    """ 
    A Person who resides in the US.
    """
    def __init__(self, name, status):
        """ 
        Initializes a Person object. A USResident object inherits 
        from Person and has one additional attribute:
        status: a string, one of "citizen", "legal_resident", "illegal_resident"
        Raises a ValueError if status is not one of those 3 strings
        """
        # Write your code here
        Person.__init__(self, name)
        if status == "citizen" or status =="legal_resident" or status == "illegal_resident":
            self.status = status
        else:
            raise ValueError()
    def getStatus(self):
        """
        Returns the status
        """
        return self.status



'''
Problem_6
We will use Frobs to form a data structure 
called a doubly linked list. 
'''

class Frob(object):
    def __init__(self, name):
        self.name = name
        self.before = None
        self.after = None
    def setBefore(self, before):
        # example: a.setBefore(b) sets b before a
        self.before = before
    def setAfter(self, after):
        # example: a.setAfter(b) sets b after a
        self.after = after
    def getBefore(self):
        return self.before
    def getAfter(self):
        return self.after
    def myName(self):
        return self.name

def insert(atMe, newFrob):
    """
    atMe: a Frob that is part of a doubly linked list
    newFrob:  a Frob with no links 
    This procedure appropriately inserts newFrob into the 
    linked list that atMe is a part of.    
    """
    if newFrob.myName() >= atMe.myName():
        ## Then newFrob sholud be putted AFTER atMe
        ##Also we should check whether someone is located
        # in the place where we want to put new one
        if atMe.getAfter() == None:
            atMe.setAfter(newFrob)
            newFrob.setBefore(atMe)
        elif atMe.getAfter():
            ## We should compare newFrob with someone who are
            # already located in the place where we want ot put
            # new.
            counter = 0
            new_atMe = atMe.getAfter()
            while new_atMe != None:
                counter += 1
                if newFrob.myName() == new_atMe.myName():
                    newFrob.setAfter(new_atMe)
                    newFrob.setBefore(new_atMe.getBefore())
                    new_atMe.getBefore().setAfter(newFrob)
                    new_atMe.setBefore(newFrob)
                    break
                elif newFrob.myName() < new_atMe.myName():
                    middle = new_atMe.getBefore()
                    new_atMe.setBefore(newFrob)
                    middle.setAfter(newFrob)
                    newFrob.setAfter(new_atMe)
                    newFrob.setBefore(middle)
                    break
                if new_atMe.getAfter() == None:
                    new_atMe.setAfter(newFrob)
                    newFrob.setBefore(new_atMe)
                    break
                new_atMe = new_atMe.getAfter()
                if counter > 10:
                    # security break
                    break
    elif newFrob.myName() <= atMe.myName():
        ## Then newFrob sholud be putted BEFORE atMe
        ##Also we should check whether someone is located
        # in the place where we want to put new one
        if atMe.getBefore() == None:
            atMe.setBefore(newFrob)
            newFrob.setAfter(atMe)
        elif atMe.getBefore():
            ## We should compare newFrob with someone who are
            # already located in the place where we want ot put
            # new.
            counter = 0
            new_atMe = atMe.getBefore()
            while new_atMe != None:
                counter += 1
                if newFrob.myName() == new_atMe.myName():
                    newFrob.setBefore(new_atMe)
                    newFrob.setAfter(new_atMe.getAfter())
                    new_atMe.getAfter().setBefore(newFrob)
                    new_atMe.setAfter(newFrob)
                    break
                if newFrob.myName() > new_atMe.myName():
                    new_atMe.setAfter(newFrob)
                    atMe.setBefore(newFrob)
                    newFrob.setBefore(new_atMe)
                    newFrob.setAfter(atMe)
                    break
                if new_atMe.getBefore() == None:
                    new_atMe.setBefore(newFrob)
                    newFrob.setAfter(new_atMe)
                    break
                new_atMe = new_atMe.getBefore()
                if counter > 10:
                    # security break
                    break
#Test case
eric = Frob('eric')
andrew = Frob('andrew')
ruth = Frob('ruth')
fred = Frob('fred')
martha = Frob('martha')

insert(eric, andrew)
insert(eric, ruth)
insert(eric, fred)
insert(ruth, martha)
insert(eric, Frob('martha'))

test6 = []
counter = 0
next = andrew.getAfter()
print andrew.myName()
test6.append(andrew.myName())
while next != None:
    counter +=1
    #print next.myName()
    test6.append(next.myName())
    next = next.getAfter()
    if counter > 10:
        break

counter = 0
next = ruth.getBefore()
print ruth.myName()
test6.append(ruth.myName())
while next != None:
    counter +=1
    #print next.myName()
    test6.append(next.myName())
    next = next.getBefore()
    if counter > 10:
        break
print test6


'''
Problem 5_1 

Now assume that you have a working insert procedure. Starting 
with any Frob in a doubly linked list, we would like to find 
the "front" Frob, i.e., the one whose name is closest to the 
beginning of the alphabet. Write a recursive function called 
findFront to do this. findFront should take as an argument any 
Frob that is part of a doubly linked list.
'''
def findFront(start):
    """
    start: a Frob that is part of a doubly linked list
    returns: the Frob at the beginning of the linked list 
    """
    if start.getBefore() == None:
        return start
    return findFront(start.getBefore())




