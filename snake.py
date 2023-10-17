import pygame

from constants import Direction


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = Direction.UP
        self.color = "red"
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 240))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.speed = 10

    def update(self):
        if self.direction == Direction.UP:
            self.rect.y -= self.speed
        if self.direction == Direction.DOWN:
            self.rect.y += self.speed
        if self.direction == Direction.LEFT:
            self.rect.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.rect.x += self.speed
