"""
Student code for Word Wrangler game
"""

import urllib2
#import codeskulptor
import poc_wrangler_provided as provided
#import operator

WORDFILE = "assets_scrabble_words3.txt"
#Function Less-Than. return boolean
def compare_lessthen_orequal(x_element,y_element):
    '''
    function compares two elements with condition <=
    '''
    return x_element <= y_element

# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 0:
        return list1
    result = []
    lead_list = list1
    for index in range(1, len(lead_list)):
        if lead_list[index - 1] == lead_list[index]:
            continue
        else:
            if lead_list[index] != lead_list[-1]:
                result.append(lead_list[index - 1])
            else:
                result.append(lead_list[index - 1])
                result.append(lead_list[index])
    if len(result) == 0:
        result.append(list1[-1])
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    #define the shortest list from input
    # to iterate throw it
    length = min([len(list1), len(list2)])
    #Defining the name if the shortest list
    # to use it as pivot
    if len(list1) == length:
        lead_list = list1
    elif len(list2) == length:
        lead_list = list2
    else:
        lead_list = list1

    for index in range(length):
        if lead_list[index] in list2 and lead_list[index] in list1:
            result.append(lead_list[index])
    return result

# Functions to perform merge sort
def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    left, right = list1,list2 
    result = []
    ind,jin = 0,0
    #Condition that executes in shortest length times
    while ind < len(left) and jin < len(right):
        if compare_lessthen_orequal(left[ind], right[jin]):
            result.append(left[ind])
            ind += 1
        else:
            result.append(right[jin])
            jin += 1
    # Two options that winishes array that is longer 
    while (ind < len(left)):
        result.append(left[ind])
        ind += 1
    while (jin < len(right)):
        result.append(right[jin])
        jin += 1
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1[:]
    else:
        midle = int(len(list1)/2)
        #Recursively divide array until first element
        left = merge_sort(list1[: midle])
        right = merge_sort(list1[midle :])
        return merge(left, right)

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == '':
        return ['']
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    result = []
    for string in rest_strings:
        if len(string) < 1:
            result.append(first)
            continue
        gen_strings = [string[:ind] + first + string[ind:] for ind in range(len(string)+1)]
        result.extend(gen_strings)
    rest_strings.extend(result)
    return rest_strings

# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    #Desktop
    FILENAME = 'game_words.txt'
    files = open(FILENAME)
    #CodeSculptor
    #url = codeskulptor.file2url(WORDFILE)
    #files = urllib2.urlopen(url)
    
    data_list = [line[:-1] for line in files.readlines()]
    return data_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
