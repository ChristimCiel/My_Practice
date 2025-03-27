import pygame
import random

BALL_RADIUS = 7

class Ball:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BALL_RADIUS*2, BALL_RADIUS*2)
        self.color = color
        self.reset_position(x, y)

    def move(self, width, height, left_paddle, right_paddle):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.y_speed *= -1

        if self.rect.colliderect(left_paddle) or self.rect.colliderect(right_paddle):
            self.x_speed *= -1

        if self.rect.left <= 0:
            return "right"
        elif self.rect.right >= width:
            return "left"

        return None

    def reset_position(self, x, y):
        self.rect.center = (x, y)
        self.x_speed = random.choice([-4, 4])
        self.y_speed = random.choice([-4, 4])

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)