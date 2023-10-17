import pygame

import constants as c
from snake import Snake

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Reinforcement Learning')
    snake = Snake()
    group = pygame.sprite.Group()
    group.add(snake)
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        group.update()
        group.draw(screen)
        pygame.display.update()
        clock.tick(30)