import pygame, sys
from pygame.locals import *

def final():
    while True:
        pygame.init()
        screen = pygame.display.set_mode((1024, 768))
        screen.fill(0,0,0)
        font = pygame.font.SysFont("comicsansms", 35)
        victory_text = font.render('Congratulations! Thanks for Playing!', 1, (0, 255, 0))
        screen.blit(victory_text, (60, 384))
        pygame.display.flip()
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            if event.key == K_ESCAPE:
                sys.exit(0) # quit the game
