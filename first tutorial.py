import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()  # initiates pygame

pygame.display.set_caption('Night Life')

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

player_image = pygame.image.load('player.png')

while True:  # game loop

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)