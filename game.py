import pygame

import constants as c
from snake import Snake
from apple import Apple


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Snake Reinforcement Learning')

        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.snake = Snake()
        self.apple = Apple()
        
        self.clock = pygame.time.Clock()

        self.main_loop()

    def main_loop(self):
        direction = self.snake.direction
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.snake.direction != c.Direction.DOWN:
                            direction = c.Direction.UP
                    if event.key == pygame.K_DOWN:
                        if self.snake.direction != c.Direction.UP:
                            direction = c.Direction.DOWN
                    if event.key == pygame.K_LEFT:
                        if self.snake.direction != c.Direction.RIGHT:
                            direction = c.Direction.LEFT
                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction != c.Direction.LEFT:
                            direction = c.Direction.RIGHT
            
            self.snake.direction = direction
            self.screen.fill((0, 0, 0))
            self.snake.update()
            if self.snake.check_for_collision():
                break
            self.apple.draw(self.screen)
            self.snake.draw(self.screen)
            self.snake.has_eaten(self.apple)
            pygame.display.update()
            self.clock.tick(10)