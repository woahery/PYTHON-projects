import pygame
import os
import math
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2-Player Obby - Teamwork Required!")

# Player 1 setup (Red - Arrow Keys)
player1 = pygame.Rect((50, SCREEN_HEIGHT - 100, 30, 30))
player1_gravity = 0
player1_speed = 3
jump_strength = -12

# Player 2 setup (Blue - WASD)
player2 = pygame.Rect((100, SCREEN_HEIGHT - 100, 30, 30))
player2_gravity = 0
player2_speed = 3

# Game state
game_state = "playing"  # "playing" or "win"
wall_active = True  # Wall blocks path initially

# Colors
PLAYER1_COLOR = (255, 0, 0)  # Red
PLAYER2_COLOR = (0, 0, 255)  # Blue
PLATFORM_COLOR = (100, 100, 100)  # Gray
WIN_PLATFORM_COLOR = (255, 215, 0)  # Gold
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
TEXT_COLOR = (255, 255, 255)  # White
BUTTON_COLOR = (255, 100, 100)  # Light red
BUTTON_PRESSED_COLOR = (100, 255, 100)  # Light green
WALL_COLOR = (150, 50, 50)  # Dark red

# Handle background image loading
try:
    background = pygame.image.load('PNGAVIF.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    has_background = True
    print("Background image loaded successfully!")
except (pygame.error, FileNotFoundError) as e:
    print(f"Background image not found or couldn't be loaded: {e}")
    has_background = False

# Create platforms for the obby (x, y, width, height)
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground floor
    pygame.Rect(200, SCREEN_HEIGHT - 150, 120, 20),        # Platform 1
    pygame.Rect(450, SCREEN_HEIGHT - 280, 120, 20),        # Platform 2
    pygame.Rect(700, SCREEN_HEIGHT - 410, 120, 20),        # Platform 3
    pygame.Rect(950, SCREEN_HEIGHT - 540, 120, 20),        # Platform 4
    pygame.Rect(200, SCREEN_HEIGHT - 670, 120, 20),        # Platform 5
    pygame.Rect(250, SCREEN_HEIGHT - 630, 120, 20),        # Platform 9
    pygame.Rect(500, SCREEN_HEIGHT - 600, 120, 20),        # Platform 6
    pygame.Rect(550, SCREEN_HEIGHT - 550, 120, 20),        # Platform 8
    pygame.Rect(800, SCREEN_HEIGHT - 700, 120, 20),        # Platform 7 (button platform)
]

# Button on platform 7
button = pygame.Rect(830, SCREEN_HEIGHT - 720, 60, 20)

# Wall that blocks the path (disappears when button is pressed)
wall = pygame.Rect(400, SCREEN_HEIGHT - 800, 20, 130)

# Win zone (ceiling area)
win_zone = pygame.Rect(180, 0, 140, 30)

# Font for text
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()

def reset_game():
    global player1, player1_gravity, player2, player2_gravity, game_state, wall_active
    player1 = pygame.Rect((50, SCREEN_HEIGHT - 100, 30, 30))
    player1_gravity = 0
    player2 = pygame.Rect((100, SCREEN_HEIGHT - 100, 30, 30))
    player2_gravity = 0
    game_state = "playing"
    wall_active = True

def draw_game():
    # Draw background
    if has_background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BACKGROUND_COLOR)
    
    if game_state == "playing":
        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)
        
        # Draw button (changes color when pressed)
        button_pressed = player2.colliderect(button)
        button_color = BUTTON_PRESSED_COLOR if button_pressed else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button)
        
        # Draw wall (only if active)
        if wall_active:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        
        # Draw win zone
        pygame.draw.rect(screen, WIN_PLATFORM_COLOR, win_zone)
        
        # Draw players
        pygame.draw.rect(screen, PLAYER1_COLOR, player1)
        pygame.draw.rect(screen, PLAYER2_COLOR, player2)
        
        # Draw instructions
        instruction_text = font.render("RED: Arrow Keys | BLUE: WASD | Blue must stand on button to remove wall!", True, TEXT_COLOR)
        screen.blit(instruction_text, (10, 10))
        
        instruction_text2 = font.render("Red player reaches the GOLD ceiling to win! Press R to restart", True, TEXT_COLOR)
        screen.blit(instruction_text2, (10, 35))
        
        # Draw button status
        if button_pressed:
            status_text = font.render("BUTTON PRESSED - WALL REMOVED!", True, (0, 255, 0))
        else:
            status_text = font.render("Blue player must press the button!", True, (255, 255, 0))
        screen.blit(status_text, (10, 65))
        
    elif game_state == "win":
        # Win screen
        screen.fill((0, 100, 0))  # Green background
        
        # Draw celebration text
        win_text = big_font.render("TEAMWORK WINS!", True, (255, 255, 0))
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(win_text, win_rect)
        
        congrats_text = font.render("blue carried", True, TEXT_COLOR)
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        screen.blit(congrats_text, congrats_rect)
        
        restart_text = font.render("press R to play again or ESC to quit", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        screen.blit(restart_text, restart_rect)

def update_player(player_rect, gravity, keys, up_key, left_key, right_key):
    # Horizontal movement
    if keys[left_key]:
        player_rect.move_ip(-player1_speed, 0)
    if keys[right_key]:
        player_rect.move_ip(player1_speed, 0)
    
    # Apply gravity
    gravity += 0.5
    player_rect.move_ip(0, int(gravity))
    
    # Check platform collisions
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and gravity > 0:
            player_rect.bottom = platform.top
            gravity = 0
            on_ground = True
            break
    
    # Check wall collision (only if wall is active)
    if wall_active and player_rect.colliderect(wall):
        # Push player back from wall
        if player_rect.centerx < wall.centerx:
            player_rect.right = wall.left
        else:
            player_rect.left = wall.right
    
    # Jumping (only when on ground)
    if keys[up_key] and on_ground:
        gravity = jump_strength
    
    # Keep player within screen bounds horizontally
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    
    return gravity

def update_players():
    global player1_gravity, player2_gravity, game_state, wall_active
    
    if game_state != "playing":
        return
    
    # Get key inputs
    keys = pygame.key.get_pressed()
    
    # Update both players
    player1_gravity = update_player(player1, player1_gravity, keys, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT)
    player2_gravity = update_player(player2, player2_gravity, keys, pygame.K_w, pygame.K_a, pygame.K_d)
    
    # Check button mechanism - player 2 must be on button to deactivate wall
    wall_active = not player2.colliderect(button)
    
    # Check if either player falls off screen (reset)
    if player1.top > SCREEN_HEIGHT or player2.top > SCREEN_HEIGHT:
        reset_game()
    
    # Win condition - only player 1 (red) needs to reach the win zone
    if player1.colliderect(win_zone):
        game_state = "win"

# Main game loop
run = True
while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_ESCAPE and game_state == "win":
                run = False
    
    # Update game
    update_players()
    
    # Draw everything
    draw_game()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
