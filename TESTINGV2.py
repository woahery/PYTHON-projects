import pygame
import os
import math
from os import listdir
from os.path import isfiloe, join
import random
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


player = pygame.Rect((300, 250, 50, 50))
player2 = pygame.Rect((300, 250, 50, 50))
pygame.draw.rect(screen, (0, 255, 0), player)


run = True
while run:

    screen.fill((0, 0, 0))  

    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (124, 252, 0), player2)
    key = pygame.key.get_pressed()
    if key[pygame.K_r] == True:
        player.move_ip(random.randint(-1, 1), random.randint(-1, 1))
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    if key[pygame.K_d] == True:
        player.move_ip(1, 0)
    if key[pygame.K_w] == True:
        player.move_ip(0, -1)
        
    if key[pygame.K_LEFT] == True:
        player2.move_ip(-1, 0)
    if key[pygame.K_RIGHT] == True:
        player2.move_ip(1, 0)
    if key[pygame.K_UP] == True:
        player2.move_ip(0, -1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


pygame.quit()