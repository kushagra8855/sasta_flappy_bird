import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
background_image = pygame.image.load("background.png").convert()
bird_image = pygame.image.load("bird.png").convert_alpha()
pipe_image = pygame.image.load("bottom_pipe.png").convert_alpha()

# Game variables
bird_width = 34
bird_height = 24
bird_x = 50
bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
bird_speed = 5
gravity = 0.25
bird_movement = 0

pipes = []
pipe_interval = 200
pipe_speed = 3
last_pipe_time = 0

score = 0
font = pygame.font.Font(None, 36)

# Functions
def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

def draw_pipes():
    for pipe in pipes:
        screen.blit(pipe_image, pipe)

def create_pipe():
    min_pipe_gap = 80
    max_pipe_gap = 200  # Adjust the maximum gap size as needed
    pipe_gap = random.randint(min_pipe_gap, max_pipe_gap)
    pipe_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
    top_pipe = pipe_image.get_rect(midbottom=(SCREEN_WIDTH + 50, pipe_height - pipe_gap // 2))
    bottom_pipe = pipe_image.get_rect(midtop=(SCREEN_WIDTH + 50, pipe_height + pipe_gap // 2))
    return top_pipe, bottom_pipe

def move_pipes():
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]

def check_collision():
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def update_score():
    global score
    for pipe in pipes:
        if pipe.right < bird_x <= pipe.right + bird_speed:
            score += 0.5
            return

def display_score():
    score_surface = font.render(f'Score: {int(score)}', True, (0, 0, 0))
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

def game_over():
    game_over_surface = font.render(f'Game Over! Score: {int(score)}', True, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_over_surface, game_over_rect)
    retry_surface = font.render("Press SPACE to try again", True, (255, 255, 255))
    retry_rect = retry_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(retry_surface, retry_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False

def reset_game():
    global bird_y, pipes, score, bird_movement
    bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
    pipes = []
    score = 0
    bird_movement = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 4 # Bird jumps

    # Update bird position
    bird_movement += gravity
    bird_y += bird_movement
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    bird_rect.inflate_ip(-10, -10)

    # Generate pipes
    if pygame.time.get_ticks() - last_pipe_time > 2000:
        pipes.extend(create_pipe())
        last_pipe_time = pygame.time.get_ticks()

    # Redraw the screen
    screen.blit(background_image, (0, 0))

    # Move and draw pipes
    pipes = move_pipes()
    draw_bird(bird_x, bird_y)
    draw_pipes()

    # Check for collisions
    if check_collision():
        if game_over():
            break
        if not game_over():
            reset_game()

    # Update score
    update_score()
    display_score()



    # Update the display
    pygame.display.update()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
