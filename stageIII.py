#Copyright (C) 2018  Wonsik Nam
#Part of RACING MAZE game

#initialize the screen
import pygame, math, sys, time, stageIII
from pygame.locals import *

display = pygame.display.set_mode((1024, 768))
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def quitgame():
    pygame.quit()
    quit()

def button(message,x,y,w,h,normal_color,bright_color, focus = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        pygame.draw.rect(display, bright_color,(x,y,w,h)) #When the mouse cursor is over the button
        if click[0] == True and focus != None:
            focus()
    else:
        pygame.draw.rect(display, normal_color,(x,y,w,h)) #Normal color of the buttons when the cursor is not over the buttons

    buttonText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(message, buttonText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display.blit(textSurf, textRect)

pause = False
def unpause():
    global pause
    pause = False

def paused():
    clock = pygame.time.Clock() #game clock
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = (500,330)
    display.fill(black)
    display.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue",280,450,100,50,green,bright_green,unpause)
        button("Quit",600,450,100,50,red,bright_red,quitgame)

        pygame.display.flip()
        clock.tick(25)

def stageIII():
    global pause
    pygame.mixer.init()
    pygame.mixer.music.load('/Users/david/Documents/NEED_FOR_SPEED.m4a')
    pygame.mixer.music.play()
    screen = pygame.display.set_mode((1024, 768)) #screen size
    clock = pygame.time.Clock() #game clock
    victory = None

    class Player(pygame.sprite.Sprite):
        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image)
            self.rect = self.src_image.get_rect()
            self.position = position
            self.speed = 0
            self.MAX_SPEED = 9.5
            self.direction = 0
            self.k_left = 0
            self.k_right = 0
            self.k_down = 0
            self.k_up = 0

        def update(self, time):
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_SPEED:
                self.speed = self.MAX_SPEED
            if self.speed < -self.MAX_SPEED:
                self.speed = -self.MAX_SPEED
            self.direction += self.k_right + self.k_left
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            x -= self.speed*math.sin(rad)
            y -= self.speed*math.cos(rad)
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

    #Create a car for the player
    rect = screen.get_rect()
    car = Player('/Users/david/Documents/car.png', (10, 725))
    car_group = pygame.sprite.Group(car)

    class SmallVerticalWall(pygame.sprite.Sprite):
        small_vertical_walls = pygame.image.load('/Users/david/Documents/small_vertical_walls.png')
        collision = pygame.image.load('/Users/david/Documents/collision.png')
        def __init__(self, position):
            super(SmallVerticalWall, self).__init__()
            self.rect = pygame.Rect(self.small_vertical_walls.get_rect())
            self.rect.center = position
        def update(self, hit_list):
            if self in hit_list:
                self.image = self.collision
            else:
                self.image = self.small_vertical_walls

    class SmallVerticalWall2(pygame.sprite.Sprite):
        small_vertical_walls = pygame.image.load('/Users/david/Documents/small_vertical_walls2.png')
        collision = pygame.image.load('/Users/david/Documents/collision.png')
        def __init__(self, position):
            super(SmallVerticalWall2, self).__init__()
            self.rect = pygame.Rect(self.small_vertical_walls.get_rect())
            self.rect.center = position
        def update(self, hit_list):
            if self in hit_list:
                self.image = self.collision
            else:
                self.image = self.small_vertical_walls

    class VerticalWall(pygame.sprite.Sprite):
        vertical_walls = pygame.image.load('/Users/david/Documents/vertical_walls.png')
        collision = pygame.image.load('/Users/david/Documents/collision.png')
        def __init__(self, position):
            super(VerticalWall, self).__init__()
            self.rect = pygame.Rect(self.vertical_walls.get_rect())
            self.rect.center = position
        def update(self, hit_list):
            if self in hit_list:
                self.image = self.collision
            else:
                self.image = self.vertical_walls

    class WallSprite(pygame.sprite.Sprite):
        walls = pygame.image.load('/Users/david/Documents/walls.png')
        collision = pygame.image.load('/Users/david/Documents/collision.png')
        def __init__(self, position):
            super(WallSprite, self).__init__()
            self.rect = pygame.Rect(self.walls.get_rect())
            self.rect.center = position
        def update(self, hit_list):
            if self in hit_list:
                self.image = self.collision
            else:
                self.image = self.walls

    class Blinky(pygame.sprite.Sprite):
        blinky = pygame.image.load('/Users/david/Documents/Blinky.png')
        collision = pygame.image.load('/Users/david/Documents/collision.png')

        def __init__(self, x, y):
            super(Blinky, self).__init__()
            self.rect = pygame.Rect(self.blinky.get_rect())
            self.rect.x = x
            self.rect.y = y
        def update(self, hit_list):
            if self in hit_list:
                self.image = self.collision
            else:
                self.image = self.blinky

    blinky_group = pygame.sprite.Group()
    #Positioning where the Blinky's will be on the screen
    mblk1 = Blinky(600, 710)
    mblk2 = Blinky(600, 30)
    mblk3 = Blinky(40, 65)
    blinky_group.add(mblk1)
    blinky_group.add(mblk2)
    blinky_group.add(mblk3)
    blinky_speed1 = 3 #Speed of the Blinky
    blinky_speed2 = 5
    blinky_speed3 = 5

    class SmallHorizontalWall(pygame.sprite.Sprite):
        normal = pygame.image.load('/Users/david/Documents/small_horizontal_walls.png')
        def __init__(self, position):
            super(SmallHorizontalWall, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal

    class SmallVerticalWall(pygame.sprite.Sprite):
        normal = pygame.image.load('/Users/david/Documents/small_vertical_walls.png')
        def __init__(self, position):
            super(SmallVerticalWall, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal

    #level design
    walls = [
        #Vertical Walls used to set boundaries for boths end of the screen, so that when the user drives the car off the screen, the car will crash
        VerticalWall((-50,0)),
        VerticalWall((-50,400)),
        VerticalWall((-50,700)),
        VerticalWall((1080,0)),
        VerticalWall((1080,400)),
        VerticalWall((1080,700)),

        WallSprite((0, 820)), #In case the user drives off the window on the bottom of the screen

        WallSprite((0, 650)),
        WallSprite((300, 650)),
        WallSprite((550, 650)),
        SmallHorizontalWall((600,650)),
        SmallHorizontalWall((770,650)),
        SmallVerticalWall2((906,599)),
        WallSprite((990, 460)),
        SmallVerticalWall2((730,511)),
        WallSprite((470, 562)),
        SmallHorizontalWall((220,562)),
        SmallVerticalWall((105,450)),
        WallSprite((-40, 250)),
        SmallVerticalWall2((218,301)),
        SmallVerticalWall2((218,380)),
        SmallHorizontalWall((430,470)),
        WallSprite((580, 375)),
        SmallVerticalWall((550,240)),
        SmallVerticalWall((649,240)),
        SmallHorizontalWall((358, 130)),
        SmallHorizontalWall((275, 130)),
        SmallHorizontalWall((837, 130)),


    ]

    wall_group = pygame.sprite.Group(*walls)

    class Trophy(pygame.sprite.Sprite):
        def __init__(self, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('/Users/david/Documents/trophy.png')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = position
        def draw(self, screen):
            screen.blit(self.image, self.rect)

    trophy = [Trophy((590,315))] #Position of the Trophy
    trophy_group = pygame.sprite.Group(*trophy)

    font = pygame.font.SysFont("comicsansms", 35)
    font2 = pygame.font.SysFont("comicsansms", 15)
    victory_text = font.render('', 1, (0, 255, 0))
    loss_text = font.render('', 1, (229, 0, 16))
    pause_text = font.render('', 1, (0, 255, 0))
    t1 = time.time()

    #Game Loop
    while True:
        t2 = time.time()
        deltat = t2-t1
        update_clock = clock.tick(25)
        #In the event of the user pressing a key
        for event in pygame.event.get():
            #Just continue if the appropriate key isn't pressed
            if not hasattr(event, 'key'):
                continue
            key_down = event.type == KEYDOWN
            if victory == None:
                if event.key == K_RIGHT:
                    car.k_right = key_down * -6
                elif event.key == K_LEFT:
                    car.k_left = key_down * 6
                elif event.key == K_UP:
                    car.k_up = key_down * 1.5
                elif event.key == K_DOWN:
                    car.k_down = key_down * -1.5
                elif event.key == K_p:
                    pause = True
                    paused()
                elif event.key == K_ESCAPE:
                    sys.exit(0) #Exit Game
            elif victory == True and event.key == K_SPACE:
                time.sleep(0.4)
                final.final() #Move to the final ending page
            elif victory == False and event.key == K_SPACE:
                time.sleep(0.4)
                blinky_group.remove(mblk1)
                blinky_group.remove(mblk2)
                blinky_group.remove(mblk3)
                stageIII() #Restart the current level
                t1 = t2
            elif event.key == K_ESCAPE:
                sys.exit(0)

        #Countdown Timer
        seconds = round((60 - deltat), 1)
        if victory == None:
            timer_text = font.render(str(seconds), True, (0,255,0))
            #When time is up:
            if seconds <= 0:
                victory = False
                timer_text = font.render("Time's Up!", True, (229,0,16))
                loss_text = font.render('Press Space to Retry', True, (229,0,16))
                car.MAX_SPEED = 0
                car.k_right = 0
                car.k_left = 0
                blinky_speed1 = 0
                blinky_speed2 = 0
                blinky_speed3 = 0

        #FPS reading
        text_fps = font2.render('FPS: ' + str(int(clock.get_fps())), True, (0, 127, 255))

        screen.fill((255,255,255))
        car_group.update(update_clock)

        #In collision with the wall
        collisions = pygame.sprite.groupcollide(car_group, wall_group, False, False, collided = None)
        if collisions != {}:
            victory = False
            timer_text = font.render("You have crashed!", True, (229,0,16))
            car.image = pygame.image.load('/Users/david/Documents/collision.png')
            loss_text = font.render('Press Space to Retry', True, (229,0,16))
            seconds = 0
            #after crash, make sure the car isn't able to move by the user
            car.MAX_SPEED = 0
            car.k_right = 0
            car.k_left = 0
            blinky_speed1 = 0
            blinky_speed2 = 0
            blinky_speed3 = 0

        #When you have been able to successfully hit the trophy
        trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True, collided = None)
        if trophy_collision != {}:
            seconds = seconds
            timer_text = font.render("Finished!", True, (0,255,0))
            victory = True
            car.MAX_SPEED = 0
            #pygame.mixer.music.play(loops=0, start=0.0)
            victory_text = font.render('Press Space to Advance', True, (0,255,0))
            blinky_speed1 = 0
            blinky_speed2 = 0
            blinky_speed3 = 0
            if victory == True:
                car.k_right = -5

        #Given horizontal limits so that the Blinky can go back and forth at a steady speed
        if mblk1.rect.y > 740:
            blinky_speed1 = -blinky_speed1
        if mblk1.rect.y < 680:
            blinky_speed1 = -blinky_speed1
        mblk1.rect.y += blinky_speed1

        if mblk2.rect.x > 670:
            blinky_speed2 = -blinky_speed2
        if mblk2.rect.x < 500:
            blinky_speed2 = -blinky_speed2
        mblk2.rect.x += blinky_speed2

        if mblk3.rect.y > 150:
            blinky_speed3 = -blinky_speed3
        if mblk3.rect.y < 25:
            blinky_speed3 = -blinky_speed3
        mblk3.rect.y += blinky_speed3

        #When the car collides with the Blinky
        blinky_collisions = pygame.sprite.groupcollide(car_group, blinky_group, False, False, collided = None)
        if blinky_collisions != {}:
            victory = False
            timer_text = font.render("You have crashed!", True, (229,0,16))
            car.image = pygame.image.load('/Users/david/Documents/collision.png')
            loss_text = font.render('Press Space to Retry', True, (229,0,16))
            seconds = 0
            #after crash, make sure the car isn't able to move by the user
            car.MAX_SPEED = 0
            car.k_right = 0
            car.k_left = 0
            blinky_speed1 = 0
            blinky_speed2 = 0
            blinky_speed3 = 0

        blinky_group.update(collisions)
        blinky_group.draw(screen)
        wall_group.update(collisions)
        wall_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        screen.blit(timer_text, (10,3))
        screen.blit(text_fps, (950,10))
        screen.blit(victory_text, (300, 690))
        screen.blit(loss_text, (300, 690))
        screen.blit(pause_text, (380, 350))
        pygame.display.flip()
