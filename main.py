import pygame

import constants as c
from snake import Snake
from apple import Apple

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Reinforcement Learning')
    snake = Snake()
    apple = Apple()
    
    running = True
    clock = pygame.time.Clock()
    direction = snake.direction
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != c.Direction.DOWN:
                        direction = c.Direction.UP
                if event.key == pygame.K_DOWN:
                    if snake.direction != c.Direction.UP:
                        direction = c.Direction.DOWN
                if event.key == pygame.K_LEFT:
                    if snake.direction != c.Direction.RIGHT:
                        direction = c.Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    if snake.direction != c.Direction.LEFT:
                        direction = c.Direction.RIGHT
        
        snake.direction = direction
        screen.fill((0, 0, 0))
        snake.update()
        apple.draw(screen)
        snake.draw(screen)
        snake.has_eaten(apple)
        running = not snake.check_for_collision()
        pygame.display.update()
        clock.tick(10)