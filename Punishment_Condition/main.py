#Imports
import sys, os
import random 
import pygame as pg
import pandas as pd
import pyxid2

from pathlib import Path

#####################
from door import *
from feedback import *

#########################
# Excel name to save
print("File Name")
FILE_NAME = input()
#########################

#Initializing 
pg.init()

# Ask for settings
print("Which test setting are you using? (A or B)")
setting = input()
if setting == 'A':
    bias_array = [[70,30], [50,50], [90,10], [30,70], [10,90]]
else:
    bias_array = [[30,70], [90,10], [50,50], [10,90], [70,30]]

#Setting up FPS 
FPS = 60
FramePerSec = pg.time.Clock()

bg_fill = (36, 36, 36)

# EEG
os.system("sudo rmmod ftdi_sio")
os.system("sudo rmmod usbserial")
devices = pyxid2.get_xid_devices()

if devices:
    print(devices)
else:
    print("No devices")
    exit()

dev = devices[0]
dev.set_pulse_duration(1)

#Create the window
screen_modes = pg.display.list_modes()
SCREEN_WIDTH = screen_modes[0][0]
SCREEN_HEIGHT = screen_modes[0][1]-50

SCREENRECT = pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_WIDTH)
SCREEN = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pg.RESIZABLE)
SCREEN.fill(bg_fill)
pg.display.set_caption("CalmBCI")

#Setting up Fonts
my_font = pg.font.SysFont('Comic Sans MS', 35, bold=True)
start_text = my_font.render('Press space to start', True, (147, 47, 47))
pause_text = my_font.render('Press space to continue', True, (147, 47, 47))

trial_font = pg.font.SysFont('Comic Sans MS', 35)
trial_text = my_font.render('1/200', True, (219, 81, 7))
trial_Rect = trial_text.get_rect()
trial_Rect.center = (50, SCREEN_HEIGHT-20)

#### Dataframe
df = pd.DataFrame(columns=['Trial', 'Start', 'Collision', 'Difference', 'Stimuli Time', 'Selection', 'Correct Door', 'Position', 'Run'])
positions_saver = []

failed_Number = 0
# Function to load the images
main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(folder, file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, folder, file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert_alpha()

class BackgroundCircles():  
      def __init__(self, path):
        self.bgimage = pg.image.load(path).convert_alpha()
        self.rectBGimg = self.bgimage.get_rect()

        self.init_pos = (random.randint(30, SCREEN.get_width()-30), random.randint(30, SCREEN.get_height()-30))
        self.bgX = self.init_pos[0]
        self.bgY = self.init_pos[1]            

        self.limit = random.randint(20, 150)
        self.movingUpSpeed = random.randrange(-1, 1, 2) * 0.5
         
      def update(self):
        self.bgY += self.movingUpSpeed
        if self.bgY > self.init_pos[1]+self.limit:
            self.movingUpSpeed = -self.movingUpSpeed
        if self.bgY < self.init_pos[1]-self.limit:
            self.movingUpSpeed = -self.movingUpSpeed
             
      def render(self):
        SCREEN.blit(self.bgimage, (self.bgX, self.bgY))

class Player(pg.sprite.Sprite):
    """The penguin"""
    
    w = 0
    speed = 8
    scaleBy = 1.0
    state = 0
    maxIter = 9
    canMove = True
    images = []

    images_waiting = []
    images_burning = []
    for i in range(9):
        images_waiting.append(pg.transform.scale_by(load_image("res/imgs/Tux", "stand-"+str(i)+".png"), scaleBy))
        images_burning.append(pg.transform.scale_by(load_image("res/imgs/Tux", "stand-burn-"+str(i)+"-5.png"), scaleBy))

    images_walking = []
    images_right = []
    images_left = []
    images_jump = []
    for i in range(8):
        images_walking.append(pg.transform.scale_by(load_image("res/imgs/Tux", "climb-"+str(i)+".png"), scaleBy))
        images_right.append(pg.transform.scale_by(load_image("res/imgs/Tux", "walk-"+str(i)+".png"), scaleBy))
        images_left.append(pg.transform.flip(pg.transform.scale_by(load_image("res/imgs/Tux", "walk-"+str(i)+".png"), scaleBy), True, False))
        images_jump.append(pg.transform.scale_by(load_image("res/imgs/Tux", "jump-"+str(i)+".png"), scaleBy))

    images_backflip = []
    for i in range(6):
        images_backflip.append(pg.transform.scale_by(load_image("res/imgs/Tux", "backflip-"+str(i)+".png"), scaleBy))

    images_buttjump = []
    images_duck = []
    for i in range(12):
        images_buttjump.append(pg.transform.scale_by(load_image("res/imgs/Tux", "buttjump-"+str(i)+".png"), scaleBy))
        images_duck.append(pg.transform.scale_by(load_image("res/imgs/Tux", "duck-"+str(i)+".png"), scaleBy))   

    x_low_limit = (SCREEN_WIDTH/2)-200
    x_high_limit = (SCREEN_WIDTH/2)+200
    y_low_limit = (SCREEN_HEIGHT/2)+220
    y_high_limit = (SCREEN_HEIGHT/2)+120

    startBurning = 0
    bolaFuego = 0
    end = 0
    times = 0

    def __init__(self):
        super().__init__() 
        self.image = self.images_waiting[0]
        self.surf = pg.Surface((68, 80))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, self.y_low_limit))
        self.walking = False
        self.iter = 0
        self.images = [self.images_waiting, 9]
    
    def getX(self):
        return self.rect[0]
    
    def getHeight(self):
        return self.rect[1]
    
    def returnToInit(self):
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, self.y_low_limit))
    
    def run(self, direction):
        # -1 para arriba
        if self.canMove:
            if direction < 0 and self.rect.bottom > self.y_high_limit:  # Limite por arriba
                leftright = 0
                if  self.rect.left < (self.x_low_limit+self.y_low_limit-self.rect.bottom):
                    leftright = 8
                elif self.rect.right > (self.x_high_limit-(self.y_low_limit-self.rect.bottom)):
                    leftright = -8
                self.rect.move_ip(leftright, -self.speed)
            elif direction> 0 and self.rect.bottom < self.y_low_limit+self.surf.get_height()/2:  # Limite por abajo
                leftright = 0
                if self.rect.left < (self.x_low_limit+self.y_low_limit-self.rect.bottom):
                    leftright = 8
                elif self.rect.right > (self.x_high_limit-(self.y_low_limit-self.rect.bottom)):
                    leftright = -8
                self.rect.move_ip(leftright, self.speed)

    def move(self, direction):
        if self.canMove:
            if direction < 0 and self.rect.left > (self.x_low_limit+self.y_low_limit-self.rect.bottom):
                self.rect.move_ip(-self.speed, 0)
                self.images = [self.images_left, 8]
                self.maxIter = 8
            elif direction > 0 and self.rect.right < (self.x_high_limit-(self.y_low_limit-self.rect.bottom)):
                self.rect.move_ip(self.speed, 0)
                self.images = [self.images_right, 8]
                self.maxIter = 8
            else:
                if self.state == 1: #self.state != 2 and self.state != 3 and self.state != 4 and self.state != 5 :
                    self.images = [self.images_walking, 8]
                    self.maxIter = 8

    def changeState(self, state):
        self.state = state
        self.iter = 0
        if self.state == 0: # Waiting
            self.images = [self.images_waiting, 9]
            self.maxIter = 9
        elif state == 1:    # Walking
            self.images = [self.images_walking, 8]
            self.maxIter = 8
        elif state == 2:    # Backflip
            self.images = [self.images_backflip, 6]
            self.maxIter = 6
        elif state == 3:    # Jump
            self.canMove = False
            self.images = [self.images_jump, 8]
            self.maxIter = 8
        elif state == 4:    # Buttjump
            self.canMove = False
            self.images = [self.images_buttjump, 12]
            self.maxIter = 12
        elif state == 5:    # Duck
            self.canMove = False
            self.images = [self.images_duck, 12]
            self.maxIter = 12
        elif state == 6:    # Burning
            self.canMove = False
            self.startBurning = pg.time.get_ticks()
            self.images = [self.images_burning, 9]
            self.maxIter = 9

    def update(self):
        if self.w%4==0:
            self.image = self.images[0][self.iter]
            self.iter += 1

            if self.state == 6:
                if (pg.time.get_ticks()-self.startBurning) < 700 and self.iter > 5:
                    self.iter = 3

            if self.iter >= self.images[1]: #self.maxIter:      
                if self.state == 2:
                    self.changeState(1)
                elif self.state > 2: # Change to waiting  
                    self.changeState(0)
                    
                self.iter = 0
        self.w += 1

class Bat(pg.sprite.Sprite):
    """The bat"""
    
    w = 0
    speed = 8
    moveHorizontal = 1
    moveVertical = 1
    fireSide = ""
    throwFire = False
    doorCorrect = False
    scaleBy = 1.0
    state = 0
    goToCenter = False
    init_pos = (SCREEN_WIDTH/2+50, SCREEN_HEIGHT/2-50)
    start_sequence = []

    images = []

    images_flying = []
    for i in range(4):
        images_flying.append(pg.transform.scale_by(load_image("res/imgs/fatbat", "fly-"+str(i)+".png"), scaleBy))

    images_burning = []
    for i in range(11):
        images_burning.append(pg.transform.scale_by(load_image("res/imgs/fatbat", "burn-"+str(i)+".png"), scaleBy))

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = self.images_flying[0]
        self.surf = pg.Surface((64, 74))
        self.rect = self.surf.get_rect(center = self.init_pos)
        self.iter = 0
        self.images = [self.images_flying, 4]

    def changeState(self, state):
        self.state = state
        self.iter = 0
        if self.state == 0: # Flying
            self.goToCenter = False
            self.images = [self.images_flying, 4]
        elif state == 1:    # Burning
            self.images = [self.images_burning, 11]

    def update(self):
        if self.goToCenter:
            if self.rect.centery < SCREEN_HEIGHT/2+48.5:
                self.rect.move_ip(0, 2)
            if self.rect.centerx < SCREEN_WIDTH/2-1.5:
                self.rect.move_ip(2, 0)
            elif self.rect.centerx > SCREEN_WIDTH/2+1.5:
                self.rect.move_ip(-2, 0)
        else:
            self.rect.move_ip(self.moveHorizontal, self.moveVertical)

        if self.w%73==0:
            self.moveVertical = -self.moveVertical
        if self.w%101==0:
            self.moveHorizontal = -self.moveHorizontal

        if self.w%4==0:
            self.image = self.images[0][self.iter]
            self.iter += 1
            if self.state == 1 and self.iter == self.images[1]-2 and self.throwFire:
                Fire.speed = (player.getHeight()-503) / 20
                Player.bolaFuego = pg.time.get_ticks()
                Fire(self.rect.center, self.fireSide)

            if self.iter >= self.images[1]:
                if self.state == 1:
                    self.rect = self.surf.get_rect(center = [self.init_pos[0]-50, self.init_pos[1]])
                    self.changeState(0)
                if self.doorCorrect:
                    self.rect = self.surf.get_rect(center = [self.init_pos[0]-50, self.init_pos[1]])
                    self.goToCenter = False
                    self.doorCorrect = False
                self.iter = 0
        self.w += 1

class Fire(pg.sprite.Sprite):
    """Fire"""

    wakeUp = True
    end = 0
    scaleBy = 1.0
    w = 0
    speed = 8

    images_waking = []
    for i in range(4):
        images_waking.append(pg.transform.scale_by(load_image("res/imgs/livefire", "waking"+str(i+1)+".png"), scaleBy))
    
    images_left = []
    images_right = []
    for i in range(8):
        images_left.append(pg.transform.scale_by(load_image("res/imgs/livefire", "f"+str(i+1)+".png"), scaleBy))
        images_right.append(pg.transform.flip(pg.transform.scale_by(load_image("res/imgs/livefire", "f"+str(i+1)+".png"), scaleBy), True, False))

    def __init__(self, pos, side):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.side = side
        self.image = self.images_waking[0]
        self.rect = self.image.get_rect(midbottom=(pos[0], pos[1]+30))
        self.defaultlife = len(self.images_waking)
        self.iter = 0
        self.images = [self.images_waking, 4]
        self.startingTime = pg.time.get_ticks()

    def update(self):
        if self.wakeUp:
            self.image = self.images[0][self.iter]
            self.iter += 1
            if self.iter >= self.images[1]:
                if self.side == "L":
                    self.images = [self.images_left, 8]
                else:
                    self.images = [self.images_right, 8]
                self.wakeUp = False
                self.iter = 0
        else:
            if self.rect.center[0] < player.rect.center[0]:
                self.rect.move_ip(self.speed,0)
            elif self.rect.center[0] > player.rect.center[0]:
                self.rect.move_ip(-self.speed,0)
            if self.rect.center[1] < player.rect.center[1]:
                self.rect.move_ip(0,self.speed)
            elif self.rect.center[1] > player.rect.center[1]:
                self.rect.move_ip(0,-self.speed)
            if self.rect.center[1] >= player.rect.center[1]-5 and self.rect.center[1] <= player.rect.center[1]+5: #and(self.rect.center[0] >= player.rect.center[0]-1 or self.rect.center[0] <= player.rect.center[0]+1):
                player.times = 5
                player.changeState(6)
                pg.mixer.Sound("res/audios/wrong.wav").play()
                self.kill()
                #print("BOLA FUEGO: ", pg.time.get_ticks()-self.startingTime)
                
            self.image = self.images[0][self.iter]
            self.iter += 1
            if self.iter >= self.images[1]: #self.maxIter:
                self.iter = 0                   
        self.w += 1


def nextTrial(playeables, currentTrial, bias):
    # Change to next trial
    currentTrial += 1

    # Place the player in starting point
    player.returnToInit()
    player.changeState(1)
    player.canMove = True
    if currentTrial < 200:
        # Set the doors to flase
        playeables[0].selected = False
        playeables[2].selected = False

        trialGap_array = [0, 37, 41, 39, 40, 43]
        trialGap = trialGap_array[bias+1]

        restar = 0
        for i in range(bias+1):
            restar += trialGap_array[i]

        if (currentTrial-restar)%trialGap == 0 and currentTrial > 0:
            bias += 1
            dev.activate_line(bitmask=260)
            print("----------------------")
        
        choice = random.choices(["L", "R"], weights=(bias_array[bias]), k=1)

        if choice[0] == 'L':
            playeables[0].selected = True
        else:
            playeables[2].selected = True

        #print(currentTrial+1, bias_array[bias], choice, playeables[0].selected, playeables[2].selected)
        print(currentTrial+1)

        for obj in playeables:
            obj.play = True
        
    return currentTrial, bias

def saveInfo(df, currentTrial, collidedDoor, correctDoor, timestamps, position):
    correct = 1
    if correctDoor:
        correct = 0

    run = False
    if timestamps[1]-timestamps[0] < 2500:
        run = True
    
    df.loc[-1 ] = [int(currentTrial), timestamps[0], timestamps[1], timestamps[1]-timestamps[0], timestamps[2], collidedDoor, correct , position, run]
    df.index =  df.index + 1 
    df = df.set_index('Trial')

def timer(time, printDoors):
    dev.activate_line(bitmask=250)
    timer_start = pg.time.get_ticks()
    wait = True
    while wait:
        # Draw background first        
        SCREEN.fill(bg_fill)
        for circle in circlesArray:
            circle.update()
            circle.render()
        SCREEN.blit(pasarela, ((SCREEN_WIDTH-1280)/2, (SCREEN_HEIGHT-960)/2))

        if printDoors:
            for entity in door_sprites:
                SCREEN.blit(entity.image, entity.rect)

        for entity in player_sprite:
            entity.update()
            SCREEN.blit(entity.image, entity.rect)
        
        SCREEN.blit(trial_text, trial_Rect)
        pg.display.update()
        FramePerSec.tick(FPS)

        current_time = (pg.time.get_ticks()-timer_start) 
        if current_time>time:
            dev.activate_line(bitmask=251)
            break        

def pause():
    dev.activate_line(bitmask=240)
    wait = True
    player.changeState(0)
    while wait:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player.changeState(1)
                dev.activate_line(bitmask=241)
                wait = False
            
        # Draw background first        
        SCREEN.fill(bg_fill)
        for circle in circlesArray:
            circle.update()
            circle.render()
        SCREEN.blit(pasarela, ((SCREEN_WIDTH-1280)/2, (SCREEN_HEIGHT-960)/2))

        for entity in player_sprite:
            entity.update()
            SCREEN.blit(entity.image, entity.rect)

        SCREEN.blit(pause_text, (SCREEN_WIDTH/2-140,SCREEN_HEIGHT/2+100))
        SCREEN.blit(trial_text, trial_Rect)

        pg.display.update()
        FramePerSec.tick(FPS)   

#######################################################################################################################
# End of classes/functions
#######################################################################################################################

#### Background
circlesArray = []
for p in Path('res/imgs/spheres').glob('*.png'):
    newCircle = BackgroundCircles("res/imgs/spheres/"+p.name)
    circlesArray.append(newCircle)
    newCircle = BackgroundCircles("res/imgs/spheres/"+p.name)
    circlesArray.append(newCircle)

pasarela = pg.image.load("res/imgs/pasarela_av.png").convert_alpha()

############### INDECISION IMAGES
for i in range(25):   
    img = pg.transform.scale_by(load_image("res/imgs/indecision", "ind_"+str(i+1)+".png"), 0.1)
    Indecision.images.append(img)



#### Player
player = Player()
bat = Bat()

##### Doors
LeftDoor.baseImage = load_image("res/imgs", "Door_L_new.png")
door_L = LeftDoor((SCREEN_WIDTH, SCREEN_HEIGHT))
for i in range(14):
    newImage = load_image("res/imgs/door_L_fade", "L_"+str(i)+".png")
    door_L.passImages.append(newImage)

RightDoor.baseImage = load_image("res/imgs", "Door_R_new.png")
door_R = RightDoor((SCREEN_WIDTH, SCREEN_HEIGHT))
for i in range(14):
    newImage = load_image("res/imgs/door_R_fade", "R_"+str(i)+".png")
    door_R.passImages.append(newImage)

DoorCenter.baseImage = load_image("res/imgs", "Door_center.png")
for i in range(22):
    newImage = load_image("res/imgs/door_center", "center_"+str(i)+".png")
    DoorCenter.images.append(newImage)
DoorCenter.containers = all
door_center = DoorCenter((SCREEN_WIDTH, SCREEN_HEIGHT))

#Creating Sprites Groups
all_sprites = pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(bat)
all_sprites.add(door_L)
all_sprites.add(door_R)
all_sprites.add(door_center)

player_sprite = pg.sprite.Group()
player_sprite.add(player)
player_sprite.add(bat)

door_sprites = pg.sprite.Group()
door_sprites.add(door_L)
door_sprites.add(door_R)
door_sprites.add(door_center)

Indecision.containers = all_sprites, player_sprite
Fire.containers = all_sprites, player_sprite

#######################################################################################################################
# Bucle de esperar
start = False
dev.activate_line(bitmask=20)
while not start:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            player.changeState(0)
            dev.activate_line(bitmask=21)
            start = True
    
    SCREEN.fill(bg_fill)
    for circle in circlesArray:
        circle.update()
        circle.render()

    SCREEN.blit(pasarela, ((SCREEN_WIDTH-1280)/2, (SCREEN_HEIGHT-960)/2))
    #Moves and Re-draws all Sprites
    for entity in player_sprite:
        entity.update()
        SCREEN.blit(entity.image, entity.rect)

    SCREEN.blit(start_text, (SCREEN_WIDTH/2-120,SCREEN_HEIGHT/2+100))
         
    pg.display.update()
    FramePerSec.tick(FPS)

#######################################################################################################################
play = True
currentTrial = -1
startFrame = -1.0
bias = 0
collisionDone = False

fireTime = -3000
collisionTime = 0
stimuliStartTime = 0
collidedDoor = -2
correctDoor = False
savePosition = (0,0)
playerPosition = 550

while play:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()

    if not door_center.play:
        #Trial starts
        dev.activate_line(bitmask=200)

        # Waiting 1250 miliseconds before doors appear
        timeToAdd = (playerPosition-550)*11
        timer(1250+timeToAdd, False)

        stimuliTime = pg.time.get_ticks() - stimuliStartTime

        # Creating next trial
        collisionDone = False
        currentTrial, bias= nextTrial([door_L, door_center, door_R], currentTrial, bias)
        if currentTrial > 0:
            saveInfo(df, currentTrial, collidedDoor, correctDoor, [startFrame, collisionTime, stimuliTime], savePosition)

        # Pause the game in the 100th trial
        if currentTrial == 100:
            pause()

        if currentTrial == 200:
            df.to_excel(FILE_NAME+"_aversive.xlsx")
            df_positions = pd.DataFrame(positions_saver)
            df_positions.to_excel(FILE_NAME+"_aversive_positions.xlsx")

            print("Falladas: " + str(failed_Number))

            play = False

        startFrame = pg.time.get_ticks()
        # Doors appear
        dev.activate_line(bitmask=210)

    # Collisions
    if not collisionDone:  
        ## Center
        if pg.sprite.collide_rect(player, door_center) and abs(player.rect.bottom - door_L.rect.bottom) <= 5:
            # Choque
            dev.activate_line(bitmask=220)
            # Data to save
            collisionTime = pg.time.get_ticks()
            savePosition = player.rect.midbottom
            collidedDoor = 0
            correctDoor = door_L.selected  
            
            bat.goToCenter = True
            collisionDone = True
            player.changeState(0)
            playerPosition = player.getHeight()
            timer(1000+random.randint(-200,200), True)

            stimuliStartTime = pg.time.get_ticks()
            dev.activate_line(bitmask=231)
            Indecision(player.rect.midtop)
            bat.doorCorrect = True
            player.changeState(5)
        else:
            ## Left door
            if pg.sprite.collide_rect(player, door_L) and abs(player.rect.bottom - door_L.rect.bottom) <= 5:
                # Choque
                dev.activate_line(bitmask=220)
                # Data to save
                collisionTime = pg.time.get_ticks()
                savePosition = player.rect.midbottom
                collidedDoor = -1
                correctDoor = door_L.selected
                
                bat.goToCenter = True
                player.changeState(0)
                playerPosition = player.getHeight()
                timer(1000+random.randint(-200,200), True)
                dev.activate_line(bitmask=230)
                door_L.doorCollided()
                if door_L.selected:
                    bat.doorCorrect = True
                    stimuliStartTime = pg.time.get_ticks()
                    dev.activate_line(bitmask=233)
                    pg.mixer.Sound("res/audios/correct.wav").play() 
                    player.changeState(3)
                else:
                    stimuliStartTime = pg.time.get_ticks()
                    dev.activate_line(bitmask=234)
                    bat.throwFire = True
                    bat.fireSide = "L"
                    fireTime = pg.time.get_ticks()
                    bat.changeState(1)
                    player.changeState(4)
                    failed_Number += 1
                collisionDone = True

            ## Right door
            if pg.sprite.collide_rect(player, door_R) and abs(player.rect.bottom  - door_R.rect.bottom ) <= 5:
                # Choque
                dev.activate_line(bitmask=220)
                # Data to save
                collisionTime = pg.time.get_ticks()
                savePosition = player.rect.midbottom
                collidedDoor = 1
                correctDoor = door_L.selected
                
                bat.goToCenter = True
                player.changeState(0)
                playerPosition = player.getHeight()
                timer(1000+random.randint(-200,200), True)
                dev.activate_line(bitmask=232)
                door_R.doorCollided()
                if door_R.selected:
                    bat.doorCorrect = True
                    stimuliStartTime = pg.time.get_ticks()
                    dev.activate_line(bitmask=233)
                    pg.mixer.Sound("res/audios/correct.wav").play()
                    player.changeState(3)
                else:
                    stimuliStartTime = pg.time.get_ticks()
                    dev.activate_line(bitmask=234)
                    bat.throwFire = True
                    bat.fireSide = "R"
                    bat.changeState(1)
                    player.changeState(4)
                    failed_Number += 1
                collisionDone = True

    # Draw background first        
    SCREEN.fill(bg_fill)
    for circle in circlesArray:
        circle.update()
        circle.render()

    SCREEN.blit(pasarela, ((SCREEN_WIDTH-1280)/2, (SCREEN_HEIGHT-960)/2))
 
    # Get keys
    keystate = pg.key.get_pressed()
    # Left and right
    player.move(keystate[pg.K_RIGHT] - keystate[pg.K_LEFT])
    # Run
    player.run(keystate[pg.K_DOWN] - keystate[pg.K_UP])

    positions_saver.append((currentTrial+1, pg.time.get_ticks(), player.rect.midbottom[0], player.rect.midbottom[1]))
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.update()

    if door_center.rect.bottom < player.rect.bottom:
        for entity in door_sprites:
            SCREEN.blit(entity.image, entity.rect)
        # Draw player
        for entity in player_sprite:
            SCREEN.blit(entity.image, entity.rect)
    else:
        for entity in player_sprite:
            SCREEN.blit(entity.image, entity.rect)
        # Draw doors
        for entity in door_sprites:
            SCREEN.blit(entity.image, entity.rect)

    trial_text = trial_font.render(str(currentTrial+1)+'/200', True, (219, 81, 7))
    SCREEN.blit(trial_text, trial_Rect)
    pg.display.update()
    FramePerSec.tick(FPS)