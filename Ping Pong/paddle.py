import pygame

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 5

class Paddle:
    def __init__(self, x, y, key_up, key_down):
        self.rect = pygame.Rect(x, y - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.key_up = key_up
        self.key_down = key_down
        self.score = 0

    def update(self, keys, height_limit):
        if keys[self.key_up] and self.rect.top > 0:
            self.rect.y -= paddle_speed
        if keys[self.key_down] and self.rect.bottom < height_limit:
            self.rect.y += paddle_speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
