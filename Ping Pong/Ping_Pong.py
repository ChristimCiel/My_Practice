# main.py
import pygame
from paddle import Paddle
from ball import Ball

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Table Tennis Game")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font("微軟正黑體.ttf", 50)

# Create paddles
left_paddle = Paddle(20, HEIGHT//2, pygame.K_w, pygame.K_s)
right_paddle = Paddle(WIDTH - 30, HEIGHT//2, pygame.K_UP, pygame.K_DOWN)

# Create ball
ball = Ball(WIDTH//2, HEIGHT//2, WHITE)

# Initialize scores outside the game loop
left_score = 0  # Moved outside
right_score = 0 # Moved outside

# Main game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Update paddles
    left_paddle.update(keys, HEIGHT)
    right_paddle.update(keys, HEIGHT)

    # Update ball
    scorer = ball.move(WIDTH, HEIGHT, left_paddle.rect, right_paddle.rect)
    if scorer == "right":  # Ball exits on left side, right player scores
        right_score += 1
        ball.reset_position(WIDTH//2, HEIGHT//2)
    elif scorer == "left":  # Ball exits on right side, left player scores
        left_score += 1
        ball.reset_position(WIDTH//2, HEIGHT//2)

    # Drawing
    screen.fill(BLACK)
    left_paddle.draw(screen, WHITE)
    right_paddle.draw(screen, WHITE)
    ball.draw(screen)

    # Draw scores
    left_text = font.render(f"{left_score}", True, WHITE)
    right_text = font.render(f"{right_score}", True, WHITE)
    screen.blit(left_text, (100, 50))
    screen.blit(right_text, (WIDTH - 100, 50))

    pygame.display.flip()

pygame.quit()
