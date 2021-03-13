from pygame.locals import *
import pygame
import sys

clock = pygame.time.Clock()

pygame.init()  # Inicia o game

pygame.display.set_caption("Meu primeiro jogo")

WINDOW_SIZE = (400, 400)

screen = pygame.display.set_mode(WINDOW_SIZE)  # Inicializa a janela

player = pygame.image.load(
    'assets/personagens/mulher-guerreira/Individual Sprite/idle/Warrior_Idle_1.png')

moving_right = False
moving_left = False

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(
    player_location[0], player_location[1], player.get_width(), player.get_height())
test_rect = pygame.Rect(100, 100, 100, 50) # Apenas para teste de colisão

while True:  # Loop no game
    screen.fill((146, 244, 255))

    screen.blit(player, player_location)

    if player_location[1] > WINDOW_SIZE[1]-player.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right == True:  # Movimentação
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255, 0, 0), test_rect)
    else:
        pygame.draw.rect(screen, (0, 0, 0), test_rect)

    for event in pygame.event.get():  # Evento loop
        if event.type == QUIT:  # Checa o evento fechar da janela
            pygame.quit()  # Para o jogo
            sys.exit()  # Para o script

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
    clock.tick(60)  # Quantidade de frames por segundo
