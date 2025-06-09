import pygame
import os
import math

import random
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


player = pygame.Rect((300, 250, 50, 50))
player2 = pygame.Rect((300, 250, 50, 50))
pygame.draw.rect(screen, (0, 255, 0), player)
floor_color = (100, 100, 100)
floor_x = 0
floor_height = 50
floor_y = SCREEN_HEIGHT - 50 
floor_width = SCREEN_WIDTH
floor_rect = pygame.Rect(floor_x, floor_y, floor_width, floor_height)

player2_gravity = 0
 

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

    if player2.colliderect(floor_rect):
        player2_gravity = 0
        if key[pygame.K_LEFT] == True:
            player2.move_ip(-1, 0)
        if key[pygame.K_RIGHT] == True:
            player2.move_ip(1, 0)
        if key[pygame.K_UP] == True:
            player2.move_ip(0, -2)
        if key[pygame.K_DOWN] == True:
            player2.move_ip(0, 0)
    elif not player2.colliderect(floor_rect):
        if key[pygame.K_LEFT] == True:
            player2.move_ip(-1, 0)
        if key[pygame.K_RIGHT] == True:
            player2.move_ip(1, 0)
        if key[pygame.K_UP] == True:
            player2.move_ip(0, -1)
        if key[pygame.K_DOWN] == True:
            player2.move_ip(0, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.draw.rect(screen, floor_color, floor_rect)

    player2_gravity += .015
    player2.move_ip(0, (player2_gravity))

    pygame.display.flip()
    #if player2.colliderect(floor_rect):
        #print('collision')
    if player2.colliderect(floor_rect):
        print('BOOM')
    
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    #if player2.colliderect(floor_rect):
        
pygame.quit()

while player2.colliderect(floor_rect):
    if key[pygame.K_DOWN] == True:
        player2.move_ip(0, 0)
    if key[pygame.K_LEFT] == True:
        player2.move_ip(-1, 0)
    if key[pygame.K_RIGHT] == True:
        player2.move_ip(1, 0)
    if key[pygame.K_UP] == True:
        player2.move_ip(0, -1)
