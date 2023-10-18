import random

import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH, BLOCK_SIZE, SNAKE_COLOR, APPLE_COLOR


class Apple():
    def __init__(self):
        self.reset_apple()

    def reset_apple(self):
        self.x = random.randrange(0, WINDOW_WIDTH-1, BLOCK_SIZE)
        self.y = random.randrange(0, WINDOW_HEIGHT-1, BLOCK_SIZE)
        
    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, APPLE_COLOR, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE), 2)
