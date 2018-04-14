#Copyright (C) 2018  Wonsik Nam
#Part of RACING MAZE game

#initialize the screen
import pygame, sys, time, stageI, stageII, stageIII, random
from pygame.locals import *

#Start of Code
pygame.init() #Initialize

menu_screen = (640, 480) #Size of Menu Screen
display = pygame.display.set_mode(menu_screen)

#Random Mottos at the menu to poke fun at the user
mottos = ("I hope you have a fun time playing my game",
          "Come on now, let's get going!",
          "You taking all day here?",
          "Click on one of the top stages to start the game",
          "You must be bored. Hurry and play!",
         )

def menu():
    #pygame.mixer.init()
    #pygame.mixer.music.load('')
    #pygame.mixer.music.play() #Playing music
    Clock = pygame.time.Clock()
    Motto = random.choice(mottos)
    Font = pygame.font.SysFont("comicsansms", 20) #Font type and size
    text_motto = Font.render(Motto, True, (255,255,255))
    focus = 0
    background_color = ((255, 255, 255), (0, 0, 0))
    items = [('stageI', 'new1'), ('stageII', 'new2'), ('stageIII', 'new3'), ('Exit', 'exit')] #Different options for the user to select on the menu
    item_h = 30
    total_h = 50

    while True: #While running
        Clock.tick(25) # FPS
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return 'exit' # Quit Game
            elif event.type == MOUSEBUTTONDOWN: #When the user clicks the mouse
                if event.button==True:
                    if 300 < event.pos[0] < 400 and 20 < event.pos[1] < 140 + total_h*len(items):
                        clicked_item = int((event.pos[1] - 140)/total_h)
                        return items[clicked_item][1] #Location of the options on the screen
            elif event.type == MOUSEMOTION:
                if 250 < event.pos[0] < 450 and 20 < event.pos[1] < 140 + total_h*len(items):
                    focus = int((event.pos[1] - 140)/total_h)
            elif event.type == KEYDOWN:
                if event.key == K_DOWN: #Highlights the current item box for the user to select on the menu
                    focus = (focus + 1) % len(items)
                elif event.key == K_RIGHT:
                    focus = (focus + 1) % len(items)
                elif event.key == K_UP:
                    focus = (focus - 1) % len(items)
                elif event.key == K_LEFT:
                    focus = (focus - 1) % len(items)
                elif event.key == K_RETURN:
                    return items[focus][1]
                else:
                    pass
        display.fill((92, 144, 254))
        for n in range(len(items)): #This actually displays the menu for the user to pick from
            item_box = items[n][0]
            pygame.draw.rect(display, (255, 255, 255), (200, 140 + n*total_h, 300, item_h), 1-(focus==n))
            display.blit(Font.render(item_box, True, (background_color[focus==n])),
                         (206, 140 + n*total_h))
        #Mottos
        display.blit(text_motto,(200, 160 + total_h*len(items)))
        pygame.display.flip()

def main():
    pygame.display.set_caption("Racing Maze")
    global display
    display = pygame.display.set_mode(menu_screen)
    #Play('music')
    while True:
        result = menu()
        #When the user selects an option, it will execute
        if result == 'new1':
            if stageI.stageI() == 'exit':
                break
        elif result == 'new2':
            if stageII.stageII() == 'exit':
                break
        elif result == 'new3':
            if stageIII.stageIII() == 'exit':
                break
        elif result == 'exit':
            break
    quitgame()

if __name__ == '__main__':
    main()
