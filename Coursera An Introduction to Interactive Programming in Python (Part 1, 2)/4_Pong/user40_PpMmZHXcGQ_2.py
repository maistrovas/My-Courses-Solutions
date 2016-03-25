
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
ball_pos = [WIDTH / 2, HEIGHT / 2]
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_vel = [0, 0]
paddle1_pos = [[6,0], [6,PAD_HEIGHT]]
paddle2_pos = [[594,  0], [594, PAD_HEIGHT]]
paddle1_vel = 0
paddle2_vel = 0
y1_pad1_pos = paddle1_pos[0]
y2_pad1_pos = paddle1_pos[1]
y1_pad2_pos = paddle2_pos[0]
y2_pad2_pos = paddle2_pos[1]

x1_pad1_pos = paddle1_pos[0]
x2_pad1_pos = paddle1_pos[1]
x1_pad2_pos = paddle2_pos[0]
x2_pad2_pos = paddle2_pos[1]
p1_score = 0
p2_score = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global LEFT, RIGHT
    #ball_vel = [random.randrange(1, -3), random.randrange(-2, -4)]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4), random.randrange(-3 -1)]
    elif direction == LEFT:
        ball_vel = [random.randrange(-4, -3), random.randrange(-3 -1)]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(LEFT)
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    global ball_pos, ball_vel, BALL_RADIUS, LEFT, RIGHT, PAD_WIDTH, direction, PAD_HEIGHT, p1_score, p2_score
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_text(str(p1_score), [150, 50], 40, 'white')
    canvas.draw_text(str(p2_score), [450, 50], 40, 'white')   
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: 
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        p2_score += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] >=  WIDTH - BALL_RADIUS - PAD_WIDTH:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        p1_score += 1
        spawn_ball(LEFT)
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'red', 'white')
    # update paddle's vertical position, keep paddle on the screen
    if  PAD_HEIGHT < y2_pad1_pos[1] + paddle1_vel  <= HEIGHT and y1_pad1_pos[1] <= HEIGHT - PAD_HEIGHT:
        y2_pad1_pos[1] +=  paddle1_vel 
        y1_pad1_pos[1] += paddle1_vel 
    if  PAD_HEIGHT < y2_pad2_pos[1] + paddle2_vel <= HEIGHT and y1_pad2_pos[1] <= HEIGHT - PAD_HEIGHT:
        y2_pad2_pos[1] += paddle2_vel
        y1_pad2_pos[1] += paddle2_vel
    
    # draw paddlesa
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, 'Red')
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, 'Green')
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= x1_pad1_pos[0] + PAD_WIDTH + BALL_RADIUS and ball_pos[1]  >=  y1_pad1_pos[1] and ball_pos[1] <= y2_pad1_pos[1]:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] += 1
        ball_vel[1] -= 1 
    elif ball_pos[0] >= x1_pad2_pos[0] - PAD_WIDTH - BALL_RADIUS and ball_pos[1] >= y1_pad2_pos[1] and ball_pos[1] <= y2_pad2_pos[1] :
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] -= 1
        ball_vel[1] -= 1 
    # draw scores
def button():
    global p1_score, p2_score, ball_pos
    p1_score = 0
    p2_score = 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    new_game()
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3 
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button = frame.add_button("Restart", button, 100)

# start frame
new_game()
frame.start()
