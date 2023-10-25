import pygame

from constants import BLOCK_SIZE, APPLE_COLOR


class Apple():
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, APPLE_COLOR, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE), 2)
