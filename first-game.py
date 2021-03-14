from pygame.locals import *
import pygame
import sys

clock = pygame.time.Clock()

pygame.init()  # Inicia o game

pygame.display.set_caption("Meu primeiro jogo")

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # Inicializa a janela

display = pygame.Surface((300, 200))

moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0

player = pygame.image.load('assets/player.png')
player.set_colorkey((255, 255, 255))

player_rect = pygame.Rect(50, 50, player.get_width(), player.get_height())

grass_img = pygame.image.load('assets/grass.png')
TILE_SIZE = grass_img.get_width()

dirt_img = pygame.image.load('assets/dirt.png')

scroll = [0, 0]


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('maps/map')


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False,
                       'left': False, 'right': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


while True:  # Loop no game
    display.fill((146, 244, 255))

    scroll[0] += (player_rect.x-scroll[0]-152)/20
    scroll[1] += (player_rect.y-scroll[1]-106)/20

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_img, (x * 16-scroll[0], y * 16-scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * 16-scroll[0], y * 16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get():  # Evento loop
        if event.type == QUIT:  # Checa o evento fechar da janela
            pygame.quit()  # Para o jogo
            sys.exit()  # Para o script

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
    pygame.display.update()
    clock.tick(60)  # Quantidade de frames por segundo
