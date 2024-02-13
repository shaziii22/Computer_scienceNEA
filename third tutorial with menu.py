import pygame # import pygame
import sys # import sys

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption('Pygame Window')
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

player_image = pygame.image.load('player.png')

moving_right = False
moving_left = False

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

# Game states
MENU = 0
GAME = 1
game_state = MENU

# Menu variables
menu_font = pygame.font.Font(None, 36)
menu_option = 0

while True:
    if game_state == MENU:
        screen.fill((146, 244, 255))  # clear screen by filling it with blue

        # Handle menu events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu_option = (menu_option - 1) % 2
                elif event.key == K_DOWN:
                    menu_option = (menu_option + 1) % 2
                elif event.key == K_RETURN:
                    if menu_option == 0:  # Start option
                        game_state = GAME
                    elif menu_option == 1:  # Quit option
                        pygame.quit()
                        sys.exit()

        # Draw menu options
        start_text = menu_font.render("Start", True, (255, 255, 255) if menu_option == 0 else (128, 128, 128))
        quit_text = menu_font.render("Quit", True, (255, 255, 255) if menu_option == 1 else (128, 128, 128))
        screen.blit(start_text, (150, 150))
        screen.blit(quit_text, (150, 200))

    elif game_state == GAME:
        screen.fill((146, 244, 255))  # clear screen by filling it with blue

        screen.blit(player_image, player_location)

        if player_location[1] > WINDOW_SIZE[1] - player_image.get_height():
            player_y_momentum = -player_y_momentum
        else:
            player_y_momentum += 0.2
        player_location[1] += player_y_momentum

        if moving_right:
            player_location[0] += 4
        if moving_left:
            player_location[0] -= 4

        player_rect.x = player_location[0]
        player_rect.y = player_location[1]

        if player_rect.colliderect(test_rect):
            pygame.draw.rect(screen, (255, 0, 0), test_rect)
        else:
            pygame.draw.rect(screen, (0, 0, 0), test_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False

    pygame.display.update()
    clock.tick(60)