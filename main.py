# External modules
import sys
import pygame
from pygame.locals import *

# Internal modules
from load_map import load_map
from actions import change_action, move
from load_animation import load_animation, animation_frames

clock = pygame.time.Clock()

pygame.init() # Start the game.

pygame.display.set_caption('My game')

WINDOW_SIZE = (750, 450)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # Initialize the window.

display = pygame.Surface((300, 200))

air_timer = 0
moving_left = False
true_scroll = [0, 0]
moving_right = False
player_y_momentum = 0

animation_database = {}

animation_database['run'] = load_animation('player_animations/run', [7, 7])
animation_database['idle'] = load_animation('player_animations/idle', [7, 7, 40])

player_frame = 0
player_flip = False
player_action = 'idle'

player_rect = pygame.Rect(100,100,5,13)

game_map = load_map('maps/map')

grass_img = pygame.image.load('assets/grass.png')
TILE_SIZE = grass_img.get_width()

dirt_img = pygame.image.load('assets/dirt.png')

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [
0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]


while True:  # Loop in game
    display.fill((146, 244, 255))

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0], background_object[1]
        [1]-scroll[1]*background_object[0], background_object[1][2], background_object[1][3])

        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)

        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    tile_rects = []
    y = 0

    for row in game_map:
        x = 0

        for tile in row:
            if tile == '1': display.blit(dirt_img, (x * 16-scroll[0], y * 16-scroll[1]))
            if tile == '2': display.blit(grass_img, (x * 16-scroll[0], y * 16-scroll[1]))
            if tile != '0': tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

            x += 1

        y += 1

    player_movement = [0, 0]

    if moving_right: player_movement[0] += 2

    if moving_left: player_movement[0] -= 2

    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2

    if player_y_momentum > 3: player_y_momentum = 3

    if player_movement[0] > 0:  # Pega as ações
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False

    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0

    else:
        air_timer += 1

    player_frame += 1

    if player_frame >= len(animation_database[player_action]): player_frame = 0

    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]

    display.blit(pygame.transform.flip(player_img, player_flip, False),
    (player_rect.x -scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get():  # Event lopping.
        if event.type == QUIT:  # Check event closed window.
            pygame.quit()  # Stop game.
            sys.exit()  # Stop script

        if event.type == KEYDOWN:  # Checks if a key has been pressed.
            if event.key == K_RIGHT: moving_right = True

            if event.key == K_LEFT: moving_left = True

            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5

        if event.type == KEYUP:
            if event.key == K_RIGHT: moving_right = False

            if event.key == K_LEFT: moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)  # The amount frames in seconds.
