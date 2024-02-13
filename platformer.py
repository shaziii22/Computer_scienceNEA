import pygame, sys # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('Night Life') # set the window name

WINDOW_SIZE = (600,400) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((300, 200))


player_image = pygame.image.load('player_character.png').convert() #loads player image
player_image.set_colorkey((255, 255, 255)) # takes away any white space behind character

grass_image = pygame.image.load('grass.png') # loads grass tiles
TILE_SIZE = grass_image.get_width() # gets the width of the grass tile

dirt_image = pygame.image.load('dirt.png') # loads the dirt tile

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

def collision_test(rect, tiles):
    hit_list = [] # The list of tiles that have collided
    for tile in tiles: # checks all tiles in the list
        if rect.colliderect(tile): # if the rect has collided with the tile
            hit_list.append(tile) #add tile to hit list
    return hit_list # return list of tiles that have collided

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False} # the side that the tile has collided
    rect.x += movement[0] # moves rect on the x axis
    hit_list = collision_test(rect, tiles) # checks collision on x axis
    for tile in hit_list:
        if movement[0] > 0: # if movement was to the right
            rect.right = tile.left # aligns the sprites so that they are not inside one another
            collision_types['right'] = True # sets the right collision to true
        elif movement[0] < 0: # if movement was to the left
            rect.left = tile.right # align sprites so they are not inside one another
            collision_types['left'] = True # left collision is True
    rect.y += movement[1] # moves rect on the y axis
    hit_list = collision_test(rect, tiles) # checks collisions on y axis
    for tile in hit_list:
        if movement[1] > 0: # if movement was upward
            rect.bottom = tile.top # align sprites so they are not inside one another
            collision_types['bottom'] = True # bottom collision is True
        elif movement[1] < 0: # if movement was downward
            rect.top = tile.bottom # align sprites so they are not inside one another
            collision_types['top'] = True # Top collision is True
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

while True: # game loop
    display.fill((146,244,255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0] # initialises movement to 0 each tick
    if moving_right:
        player_movement[0] += 2 # sets movement to 2
    if moving_left:
        player_movement[0] -= 2 # sets movement to 2
    player_movement[1] += player_y_momentum # incorporates gravity
    player_y_momentum += 0.2
    if player_y_momentum > 3: # if player is moving faster than 3
        player_y_momentum = 3 # limits player movement to 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x, player_rect.y))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps
