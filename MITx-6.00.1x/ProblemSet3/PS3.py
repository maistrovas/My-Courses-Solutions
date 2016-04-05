# 6.00 Problem Set 3
# 
# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist


def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    Part 1: Is the Word Guessed
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    s = ''
    for i in secretWord:
        for j in lettersGuessed:
            if i == j:
                s +=j
                break
    lettersGuessed = s
    if lettersGuessed == secretWord:
        return True
    return False


def getGuessedWord(secretWord, lettersGuessed):
    '''
    Part 2 - Printing the User Guess
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    s = ''
    if len(lettersGuessed) == 0:
        for w in secretWord:
            s += '_'
        return s
    for i in secretWord:
        a = 0
        for j in lettersGuessed: 
            a += 1
            if i == j:
                s +=j      
                break
            if a == len(lettersGuessed): 
                s += '_'
    return s



def getAvailableLetters(lettersGuessed):
    '''
    Part 3: Printing All Available Letters
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    alfa = string.ascii_lowercase
    for i in lettersGuessed:
        alfa = alfa.replace(i, '')
    return alfa
    

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    print 'Welcome to the game Hangman!'
    print "I am thinking of a word that is " + str(len(secretWord)) + ' letters long'
    print '-----------'
    game = True
    num_trial = 8 
    player_word = ''
    not_guessed = ''
    while game:
        print 'You have ' + str(num_trial) + ' guesses left.'
        
        print 'Available Letters: ' + getAvailableLetters(player_word)
        player_guess =  raw_input('Please guess a letter:').lower()
        
        
        if player_guess in secretWord and player_guess not in player_word:               
            player_word += player_guess
            not_guessed += player_guess
            print 'Good guess: ' + getGuessedWord(secretWord, player_word)
            print '------------'
        else:
            if isWordGuessed(secretWord, player_guess) == False and player_guess in player_word:
                print "Oops! You've already guessed that letter: " + getGuessedWord(secretWord, player_word)
                print '------------'
            else:
                player_word += player_guess
                print 'Oops! That letter is not in my word: ' + getGuessedWord(secretWord, player_word)                                                                                  
                num_trial -= 1
                print '------------'
        if secretWord ==  getGuessedWord(secretWord, player_word):
            game = False
            print 'Congratulations, you won!'
            
        elif num_trial == 0:
            print 'Sorry, you ran out of guesses. The word was ' + secretWord
            game = False
        


# When you've completed your hangman function, uncomment these two lines
# and run this file to test! (hint: you might want to pick your own
# secretWord while you're testing)

secretWord = chooseWord(wordlist).lower()
hangman('camel')
