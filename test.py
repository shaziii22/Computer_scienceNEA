import pygame, sys  # import pygame and sys

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *  # import pygame modules

pygame.init()  # initiate pygame

pygame.display.set_caption('Night Life')  # set the window name

WINDOW_SIZE = (600, 400)  # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate screen

player_image = pygame.image.load('player.png')  # loads the player

moving_right = False
moving_left = False

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height()) # player rect
test_rect = pygame.Rect(160, 125, 75, 50) # position and size of rectangle

while True:  # game loop
    screen.fill((146, 244, 255))  # clear screen by filling it with blue

    screen.blit(player_image, player_location)  # render player

    # bouncy stoff
    if player_location[1] > WINDOW_SIZE[1] - player_image.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2 #fall 20 pixels
    player_location[1] += player_y_momentum

    # movement
    if moving_right == True:  #if right arrow key is pressed moving right is True
        player_location[0] += 4  #move right 20 pixels
    if moving_left == True:  #if left arrow key is pressed moving left is True
        player_location[0] -= 4  #move left 20 pixels

    player_rect.x = player_location[0]  # update rect x
    player_rect.y = player_location[1]  # update rect y

    # test rect for collisions
    if player_rect.colliderect(test_rect): # if player collides with test rectangle
        pygame.draw.rect(screen, (0,255 ,0), test_rect) # rectangle turns green
    else:
        pygame.draw.rect(screen, (0, 0, 0), test_rect)

    for event in pygame.event.get():  # event loop, checks for events

        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script

        if event.type == KEYDOWN: # if a key is pressed / put down
            if event.key == K_RIGHT: # if the key pressed is right arrow
                moving_right = True

            if event.key == K_LEFT: # if the key pressed is left arrow
                moving_left = True

        if event.type == KEYUP: # if the key is released
            if event.key == K_RIGHT: # character no longer moves right
                moving_right = False

            if event.key == K_LEFT: # character no longer moves left
                moving_left = False

    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps