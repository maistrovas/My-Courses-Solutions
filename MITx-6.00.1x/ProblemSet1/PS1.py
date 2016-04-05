'''
Problem 1: Counting Vowels
'''
vowels = ['a', 'i', 'o', 'u', 'e']
count = 0
for i in s:
    if i in vowels:
        count +=1
        
print count

'''
Problem 2: Counting 'bob's
'''
s = 'azcbobobegghakl'
def count_word_parts(word_part, word):
	'''
	Function counts number times word_part
	occurs in all woed 
	'''
    occurs = 0
    for i in range(len(word)):
        if s[i:i+3] == word_part:
            occurs +=1
    return occurs
print count_word_parts('bob', s)

'''
Problem 3: Alphabetical Substrings
Findes londest substring occurs in
alphabetical order.
'''
curString = s[0]
longest = s[0]
for i in range(1, len(s)):
    if s[i] >= curString[-1]:
        curString += s[i]
        if len(curString) > len(longest):
            longest = curString
    else:
        curString = s[i]
print 'Longest substring in alphabetical order is:', longest







