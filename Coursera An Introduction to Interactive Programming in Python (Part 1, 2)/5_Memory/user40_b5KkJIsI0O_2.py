# implementation of card game - Memory

import simplegui
import random

deck = range(0,8) * 2
num_cards = len(deck)
deck_width = 800
deck_height = 100
card_width = deck_width / num_cards
print len(deck)
# helper function to initialize globals
def new_game():
    global shuffle_list, turns, exposed_list, selected, state
    shuffle_list = list(deck)
    random.shuffle(shuffle_list)
    turns = 0
    exposed_list = [False for n in deck]
    label.set_text("Turns = 0")
    selected = []
    state = 0
     
def mouseclick(pos):
    global exposed_list, turns, state, selected
    click_index = pos[0] // card_width
    if not exposed_list[click_index]:
        if state == 0:
            state = 1
        elif state == 1 :
            turns += 1
            label.set_text("Turns =" + str(turns))
            state = 2
        else:
            if shuffle_list[selected[0]] != shuffle_list[selected[1]]:
                exposed_list[selected[0]] = exposed_list[selected[1]] = False
            selected = []     
            state = 1
        selected.append(click_index)     
        exposed_list[click_index] = True 
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card in range(0, num_cards):
        if exposed_list[card]:   
            canvas.draw_text(str(shuffle_list[card]), (card * card_width + 10, deck_height / 2 + 15) , 50, 'white')
        else:
            canvas.draw_polygon([(card * card_width, 0),
                                 ((card+1) * card_width, 0),
                                 ((card+1) * card_width, deck_height),
                                 (card * card_width, deck_height)],
                                  1, 'red', 'green')
    if all(exposed_list):
        canvas.draw_text("You win!!!", (deck_width / 2 - 70, deck_height), 30, "Red")                            
                                 
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", deck_width, deck_height)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
