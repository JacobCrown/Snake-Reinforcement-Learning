import pygame

import constants as c
from snake import Snake

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Reinforcement Learning')
    snake = Snake()
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != c.Direction.DOWN:
                        snake.direction = c.Direction.UP
                if event.key == pygame.K_DOWN:
                    if snake.direction != c.Direction.UP:
                        snake.direction = c.Direction.DOWN
                if event.key == pygame.K_LEFT:
                    if snake.direction != c.Direction.RIGHT:
                        snake.direction = c.Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    if snake.direction != c.Direction.LEFT:
                        snake.direction = c.Direction.RIGHT

        screen.fill((0, 0, 0))
        snake.update()
        snake.draw(screen)
        pygame.display.update()
        clock.tick(10)