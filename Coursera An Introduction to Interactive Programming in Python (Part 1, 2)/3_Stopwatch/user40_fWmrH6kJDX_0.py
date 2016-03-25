
#"Stopwatch: The Game"
import simplegui


# define global variables
width = 400
height = 400
interval = 100
time = '0:00.0'
t = 0
game_count = 0
win_count = 0
running = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global time
    millis = t % 10 
    sec = (t - millis) / 10 
    mins = sec // 60
    seconds = sec % 60 
    if seconds >= 10:
        time = str(mins) + ':' + str(seconds) + '.' + str(millis)
    else:
        time = str(mins) + ':0' + str(seconds) + '.' + str(millis) 
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running
    running = 1
    timer.start()

def stop():
    global game_count, win_count, running
    timer.stop()
    game_count = game_count + running
    if time[-1] == '0' and running:
        win_count = win_count + 1
    running = 0 
    

def reset():
    global t, time, game_count, win_count, running
    game_count = 0
    win_count = 0
    running = 0
    timer.stop()
    t = 0
    format(t)
    
    
#define event handler for timer with 0.1 sec interval
def timer_handler():
    global t 
    t = t + 1
    format(t)
      
    

# define draw handler
def draw(canvas):
    canvas.draw_text(time, [150, 200], 48, "red")
    canvas.draw_text(str(win_count) + '/' + str(game_count), 
                     (350, 25), 30, "Green")
    
    
# create frame
frame = simplegui.create_frame("Stopwatch", width, height)
                                          


# register event handlers
frame.add_button("Start", start,100)                               
frame.add_button("Stop", stop,100)
frame.add_button("Reset", reset,100)
frame.set_draw_handler(draw) 
timer = simplegui.create_timer(interval, timer_handler)

# start frame
frame.start()
