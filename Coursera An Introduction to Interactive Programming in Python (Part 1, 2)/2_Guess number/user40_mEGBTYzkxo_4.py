# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math
# helper function to start and restart the game
num_range = 100
def new_game():
    # initialize global variables used in your code here
    print 'New game. Range is from 0 to', num_range
    global secret_number
    secret_number = random.randrange(0,100)
    global trials
    trials = 7
    print 'Number of remaining guesses is', + trials 
   


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    print
    global num_range
    num_range = 100
    print 'New game. Range is from 0 to', num_range
    global secret_number
    secret_number = random.randrange(0,100)
    global trials
    trials = 7
    print 'Number of remaining guesses is', + trials
      

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    print
    global num_range
    num_range = 1000
    print 'New game. Range is from 0 to', num_range
    global secret_number
    secret_number = random.randrange(0,1000)
    global trials
    trials = 10
    print 'Number of remaining guesses is', + trials
    
    
def input_guess(guess):
    print
    guess = int(guess)
    print 'Guess was', + guess
    global trials
    trials -= 1
    if guess > secret_number and not trials == 0:
        print 'Number of remaining guesses is', trials
        print 'Lower!'
    elif guess < secret_number and not trials == 0:
            print 'Number of remaining guesses is', trials
            print 'Higher!'
    elif guess == secret_number:
           print 'Number of remaining guesses is', trials
           print 'Correct!'
           print
           new_game()
    else:
        print 'Number of remaining guesses is', trials
        print 'You lose!',  "The namber was", secret_number
        print
        new_game()

    

    
# create frame
frame = simplegui.create_frame('Guess the Number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range is [0, 100)', range100, 200)
frame.add_button('Rande is [0, 1000)', range1000, 200)
frame.add_input('Enter a guess', input_guess, 100)

# call new_game 
new_game()
