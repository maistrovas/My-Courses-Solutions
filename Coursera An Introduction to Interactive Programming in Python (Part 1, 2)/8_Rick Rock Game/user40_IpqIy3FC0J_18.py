# Rice Rock
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
rock_group = set ([])
missile_group = set([])
missile_collide_number = set ([])
explosion_group = set ([])
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(a_set, canvas):
    remove_set = set([])
    for sprite in a_set:
        sprite.draw(canvas)
        if sprite.update():
            remove_set.add(sprite)
            a_set.difference_update(remove_set)
    
def group_collide(group, other_object):
    global lives, explosion_group
    remove_set = set([])
    for item in group:
        if item.collide(my_ship):
            lives -= 1
    
    for item in group:
        if item.collide(other_object):
            remove_set.add(item)
            group.difference_update(remove_set)
            explosion_group.add(Sprite(item.pos, [0, 0], 0, 0, explosion_image,
                                       explosion_info, explosion_sound))
            return True
    else: 
        return False

def group_group_collide(missiles, rocks):
    global score, missile_collide_number
    for missile in missiles:
        if group_collide(rocks, missile):
            missile_collide_number.add(missile) 
            missiles.discard(missile)
    return len(missile_collide_number)
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = ship_thrust_sound
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] * 3, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        elif self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self,):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] *=(1 - 0.013)
        self.vel[1] *=(1 - 0.013)
        self.angle += self.angle_vel
        self.forward_vector = angle_to_vector(self.angle)
        
        if self.thrust == True:
            self.vel[0] += self.forward_vector[0] * 0.15
            self.vel[1] += self.forward_vector[1] * 0.15
            
    def rotate_left(self, rot_speed): 
        self.angle_vel -= rot_speed
    def rotate_right(self, rot_speed ):
        self.angle_vel += rot_speed
    def thrusters(self, thr):
        if thr:
            self.thrust = True
            self.sound.play()
        elif thr == False:
            self.thrust = False
            self.sound.pause()
    def shoot(self,):
        
        self.missile_pos = [self.pos[0] + self.forward_vector[0] * self.radius, self.pos[1] + self.forward_vector[1] * self.radius ]
        self.missile_vel = [self.vel[0]  + 6 * self.forward_vector[0], self.vel[1] + 6 * self.forward_vector[1]]
        a_missile = Sprite(self.missile_pos, self.missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    def get_position(self):
        return self.pos
    def get_radius(self):
        return self.radius
# Sprite class
class Sprite:
    
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        center = list(self.image_center)
        if self.animated:
            center[0] = self.image_center[0] + (self.image_size[0] * self.age)
        canvas.draw_image(self.image, center, self.image_size,
                         self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
    def get_position(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        return False   

def draw(canvas):
    global time, started,lives, rock_group, missile_collide_number
    global score
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
# draw ship and sprites
    my_ship.draw(canvas)
#Restart game by 'space'
    if started == True:
        soundtrack.play()
        timer.start()
        process_sprite_group(rock_group, canvas)
#Missiles and explosion draw and update
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
# update ship and sprites
    my_ship.update() 
#draw collisions rock vs. ship
    group_collide(rock_group, my_ship)
    
#draw collisions missiles vs. rocks
    group_group_collide(missile_group, rock_group)
    
    #score counter
    score = group_group_collide(missile_group, rock_group) * 25   

    #Game stop when lives off
    if lives < 0:
        started = False
        #score = 0
        lives = 3
        timer.stop()
        missile_collide_number = set([])
        rock_group = set ([])
    #global lives, score
    canvas.draw_text('Lives' + '  ' + str(lives),[WIDTH - 120, 30], 30, 'White' )
    canvas.draw_text('Score' + '  ' + str(score),[40, 30], 30, 'White')
    # Drawing splash image
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
      
    #Key handlers
def keydown(key):
    global started
    if key == simplegui.KEY_MAP['left']:
        my_ship.rotate_left(0.07)
        #started = True
    elif key == simplegui.KEY_MAP['right']:
        my_ship.rotate_right(0.07)
        #started = True
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(True)
        #started = True
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        started = True
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        ####my_ship.thrusters(False)
        my_ship.rotate_left(-0.07) 
    elif key == simplegui.KEY_MAP['right']:
        ####my_ship.thrusters(False)
        my_ship.rotate_right(-0.07)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(False)
        
# timer handler that spawns a rock each second   
def rock_spawner():
    global rock_group, score
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    while dist(rock_pos, my_ship.pos) < 100:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    ang = 0
    ang_vel = random.random() * .2 - .1
    vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    if score >= 500 and score <= 600 :
        vel[0] += random.random() * 1.6 - .3
        vel[1] += random.random() * 1.6 - .3
        
    elif score >= 700:
        vel[0] *= 10
        vel[1] *= 10
        
    a_rock = Sprite(rock_pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
    if len(rock_group) < 12: 
        rock_group.add(a_rock)
   

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info) 
# Ship and rock distance

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
