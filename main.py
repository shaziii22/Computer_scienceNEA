import pygame, sys

clock = pygame.time.Clock()

pygame.init() #initiates pygame

pygame.display.set_caption("Nightlife game") #sets name of window

WINDOW_SIZE= 600,400 #declares window size

# Setup pygame/window
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
display = pygame.Surface((300, 200))
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

font = pygame.font.SysFont(None, 40)


# Main game loop
# Game variables
game_active = False


player_momentum = [0, 0]

playerattacking = False

enemy1_image = pygame.image.load('enemy_animations/robber_runn1.png')
enemy1_location = [150, 0]
enemy1_momentum = [0,0]


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    while True:
        width = 600
        height = 400
        screen = pygame.display.set_mode((width, height))
        background_image = pygame.image.load("venv/backgrounds/Background testing.png").convert() # loads the background image
        background = pygame.transform.scale(background_image, (width, height)) # scales the image to fit the width and height
        screen.blit(background, (0, 0)) # blits the image onto the screen
        pygame.display.flip()

        draw_text("Start", font, (255, 255, 255), screen, 50, 100)
        draw_text("options", font, (255, 255, 255), screen, 50, 150)
        draw_text("quit", font, (255, 255, 255), screen, 50, 200)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 150, 200, 50)
        button_3 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game_active = True
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                quit()


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():

    global player_rect
    global game_active
    running = True
    game_active = True

    lifecooldown = 0  # Define lifecooldown
    lives = 3  # Define lives as you intend
    damagecooldown = 0  # Define damagecooldown
    enemydamage = 0  # Define enemydamage
    playerattacking = False  # Define playerattacking





    while running:
        screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)



        display = pygame.Surface((300, 200))
        if game_active == True:

            global animation_frames  # global variable
            animation_frames = {}  # animation frames dictionary

            def load_animation(path, frame_durations):  # function that takes path and frame duration as paramters
                global animation_frames  # global variable
                animation_name = path.split("/")[-1]  # takes the last word of the path
                animation_frame_data = []  # breaks down how long each image should be shown
                n = 0
                for frame in frame_durations:
                    animation_frame_id = animation_name + "_" + str(n)  # makes animation run in order from 0 up
                    img_loc = path + '/' + animation_frame_id + ".png"  # generates full path to images
                    animation_image = pygame.image.load(img_loc).convert_alpha()  # takes away whitespace of background
                    animation_frames[
                        animation_frame_id] = animation_image.copy()  # copies animation frame id to animation frame data
                    for i in range(frame):
                        animation_frame_data.append(animation_frame_id)
                    n += 1
                return animation_frame_data  # returns frame data

            def change_action(action_var, frame, new_value):
                if action_var != new_value:  # checks
                    action_var = new_value
                    frame = 0
                return action_var, frame

            animation_database = {}  # table

            animation_database['run'] = load_animation('player_animations/run',[7, 7])  # run aniations are shown for 7 frames each
            animation_database['idle'] = load_animation('player_animations/idle', [7, 7,40])  # idle animations are shown for these amounts of frames.



            player_action = "idle"
            player_frame = 0
            player_flip = False

            playerhealth_image = pygame.image.load('venv/health/player health1.png')  # Loads lives icon


            #health
            healthpos = -2
            for i in range(lives):
                healthpos += 7
                display.blit(playerhealth_image, (healthpos, 5))

            stone_image = pygame.image.load("venv/tiles/underground tile.png")
            TILE_SIZE = stone_image.get_width()
            stones_image = pygame.image.load("venv/tiles/toptile.png")

            enemydamage = 0

            game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0', '0', '0', '0', '0', '0'],
                        ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2','2', '2', '2', '2', '2', '2'],
                        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1','1', '1', '1', '1', '1', '1'],
                        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1','1', '1', '1', '1', '1', '1'],
                        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1','1', '1', '1', '1', '1', '1'],
                        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1','1', '1', '1', '1', '1', '1'],
                        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1','1', '1', '1', '1', '1', '1']]





            def collision_test(rect, tiles):
                hit_list = []
                for tile in tiles:
                    if rect.colliderect(tile):
                        hit_list.append(tile)
                return hit_list

            def move(rect, movement, tiles):
                collision_types = {"top": False, "bottom": False, "right": False, "left": False}
                rect.x += movement[0]
                hit_list = collision_test(rect, tiles)
                for tile in hit_list:
                    if movement[0] > 0:
                        rect.right = tile.left

                        collision_types["right"] = True
                    elif movement[0] < 0:
                        rect.left = tile.right
                        collision_types["left"] = True
                rect.y += movement[1]
                hit_list = collision_test(rect, tiles)
                for tile in hit_list:
                    if movement[1] > 0:
                        rect.bottom = tile.top
                        collision_types["bottom"] = True
                    elif movement[1] < 0:
                        rect.top = tile.bottom
                        collision_types["top"] = True
                return rect, collision_types


            moving_right = False
            moving_left = False

            player_y_momentum = 0
            air_timer = 0



            def xmomentum_stabilise(momentum):
                if momentum < 0.2 and momentum > -0.2:  # sets momentum to 0 after its close enough
                    momentum = 0
                elif momentum < 0:  # increments/decrements momentum such that it slowly nears 0
                    momentum += 0.2
                elif momentum > 0:
                    momentum -= 0.2
                return momentum

            player_momentum[1] = 0



            while True:  # event loop
                display.fill((1, 4, 22))

                tile_rects = []
                y = 0
                for row in game_map:
                    x = 0
                    for tile in row:
                        if tile == "1":
                            display.blit(stone_image, (x * TILE_SIZE, y * TILE_SIZE))
                        if tile == "2":
                            display.blit(stones_image, (x * TILE_SIZE, y * TILE_SIZE))
                        if tile != "0":
                            tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                        x += 1
                    y += 1

                display.blit(font.render(f'Hits Dealt: {enemydamage}', True, (255, 255, 255)), (60, 3))


                player_movement = [0, 0]
                if moving_right:
                    player_movement[0] += 2
                if moving_left:
                    player_movement[0] -= 2
                player_movement[1] += player_y_momentum
                player_y_momentum += 0.2
                if player_y_momentum > 3:
                    player_y_momentum = 3

                if player_movement[0] > 0:
                    player_action, player_frame = change_action(player_action, player_frame, "run")
                    player_flip = False
                if player_movement[0] == 0:
                    player_action, player_frame = change_action(player_action, player_frame, "idle")
                if player_movement[0] < 0:
                    player_action, player_frame = change_action(player_action, player_frame, "run")
                    player_flip = True

                player_rect = pygame.Rect(50, -20, 5,13)
                enemy1_rect = pygame.Rect(130, -20, 5,13)

                player_rect, collisions = move(player_rect, player_movement, tile_rects)
                if collisions["bottom"]:
                    if isinstance(collisions["bottom"], pygame.Rect):
                        player_y_momentum = 0
                        air_timer = 0
                        player_rect.y = collisions["bottom"].top - player_rect.height
                else:
                    air_timer += 1

                player_frame += 1
                if player_frame >= len(animation_database[player_action]):
                    player_frame = 0
                player_img_id = animation_database[player_action][player_frame]
                player_img = animation_frames[player_img_id]
                display.blit(pygame.transform.flip(player_img, player_flip, False), (player_rect.x, player_rect.y))# flips the player when facing left or right
                display.blit(pygame.transform.flip(enemy1_image, player_flip, False), (player_rect.x, player_rect.y))

                cooldown = 0


                enemy1_movement = [0, 0]  # initalises movement to 0 each tick
                enemy1_movement[1] += enemy1_momentum[1]  # incorporates gravity
                enemy1_momentum[1] += 0.4
                if enemy1_momentum[1] > 4:
                    enemy1_momentum[1] = 4  # sets max acceleration
                if player_rect[0] > enemy1_rect[0]:  # sets movement based on where the player is
                    enemy1_movement[0] += 1
                else:
                    enemy1_movement[0] -= 1

                    if player_rect.colliderect(enemy1_rect):  # function to test for collisions between two rects
                        if playerattacking:
                            enemy1_momentum[1] = -3  # sets the enemy's momentum to push them into the air
                            if player_rect[0] - 16 < enemy1_rect[0]:  # if the player is on the left of the enemy
                                player_momentum[0] -= 1  # send player leftward
                                enemy1_momentum[0] += 5  # send enemy rightward
                            else:
                                player_momentum[0] += 1  # send player rightward
                                enemy1_momentum[0] -= 5  # send enemy leftward
                            if damagecooldown > 10:
                                enemydamage += 1
                                damagecooldown = 0
                        else:
                            player_momentum[1] = -3  # sets the players momentum to push them into the air
                            if player_rect[0] - 16 < enemy1_rect[0]:  # if the player is on the left of the enemy
                                player_momentum[0] -= 2  # send player leftward
                                enemy1_momentum[0] += 4  # send enemy rightward
                            else:
                                player_momentum[0] += 2  # send player rightward
                                enemy1_momentum[0] -= 4  # send enemy leftward
                            if lifecooldown > 10:
                                lives -= 1  # LOSE A LIFE
                                lifecooldown = 0

                        if playerattacking:  # if player is attacking
                            player_attackimage = pygame.image.load('player_animations/playerattacking_0.png')  # show attacking sprite and begin countdown
                            attacktimer -= 1
                            if attacktimer < 1:  # when countdown hits 0
                                player_image = pygame.image.load('player_animations/idle_0.png')  # show normal sprite and disable attacking state
                                playerattacking = False
                                attacktimer = 10
                                cooldown = 30
                        cooldown -=1



                    player_momentum[0] = xmomentum_stabilise(player_momentum[0])
                    player_movement[0] += player_momentum[0]  # add momentum
                    enemy1_momentum[0] = xmomentum_stabilise(enemy1_momentum[0])
                    enemy1_movement[0] += enemy1_momentum[0]  # add momentum

                    enemy1_rect, enemy1_collisions = move(enemy1_rect, enemy1_movement, tile_rects)

                    if enemy1_collisions['bottom']:
                        enemy1_momentum[0] = 0

                    if enemy1_collisions['left'] or enemy1_collisions['right']:
                        enemy1_momentum[1] = -3

                player_rect, collisions = move(player_rect, player_movement, tile_rects)
                enemy1_rect, enemy1_collisions = move(enemy1_rect, enemy1_movement, tile_rects)

                # Determine the boundaries
                x_boundaryleft = 0  # Minimum x-coordinate
                x_boundaryright = 600
                max_x_right= WINDOW_SIZE[0] - player_rect.width  # Maximum x-coordinate on the right
                max_x_left = player_rect.width - WINDOW_SIZE[0]  # Maximum x-coordinate on the left


                # Check boundaries for the x-axis on the left
                if player_rect.x < x_boundaryleft:
                    player_rect.x = x_boundaryleft
                elif player_rect.x > max_x_right:
                    player_rect.x = max_x_right
                # check boundaries for the x-axis on the right
                if player_rect.x < x_boundaryright:
                    player_rect.x = x_boundaryright
                elif player_rect.x < max_x_left:
                    player_rect.x = max_x_left


                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()  # stop pygame
                        sys.exit()  # stop script
                    if event.type == KEYDOWN:
                        if event.key == K_RIGHT:
                            moving_right = True
                        if event.key == K_LEFT:
                            moving_left = True
                        if event.key == K_UP and collisions["bottom"]:
                            player_y_momentum = -5
                        if event.type == K_SPACE:
                            playerattacking = True
                    if event.type == KEYUP:
                        if event.key == K_RIGHT:
                            moving_right = False
                        if event.key == K_LEFT:
                            moving_left = False
                        if event.type == K_SPACE:
                            playerattacking = False

                            if event.type == KEYUP:
                                if event.type == K_SPACE:
                                    playerattacking = False





                surf = pygame.transform.scale(display, WINDOW_SIZE)
                screen.blit(surf, (0, 0))
                pygame.display.update()  # updates display
                clock.tick(60)  # allows game to run at 60 frames per second

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False







        pygame.display.update()
        mainClock.tick(60)


def options():
    running = True
    while running:
        width = 600
        height = 400


        background_image = pygame.image.load("venv/backgrounds/Background testing.png").convert()
        background = pygame.transform.scale(background_image, (width, height))
        screen.blit(background, (0, 0))
        pygame.display.flip()



        widthbb = 60
        heightbb = 60
        draw_text('KEY BINDS: W A S D', font, (255, 255, 255), screen,0,120)
        draw_text('ATTACK: SPACE', font ,(255, 255, 255), screen,0,160)
        backbutton = pygame.image.load('venv/images/backbutton.png')
        backbutton1 = pygame.transform.scale(backbutton, (widthbb, heightbb))
        screen.blit(backbutton1, (0,0))
        pygame.display.flip()

        mx, my = pygame.mouse.get_pos()
        backbutton_rect = pygame.Rect(0,0,60,60)
        if backbutton_rect.collidepoint((mx, my)):
            if click:
                main_menu()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: #if user presses escape
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN: #if user presses mousebutton
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)
main_menu()







