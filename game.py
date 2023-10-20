import sys
from typing import Tuple

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
        self.points = 0
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)

    def _print_points(self):
        text = self.font.render(f"Score: {self.points}",
                                True, c.TEXT_COLOR, c.BACKGROUND_COLOR)
        text_rect = text.get_rect()
        
        text_rect.topright = (c.WINDOW_WIDTH - 50, 10)
        self.screen.blit(text, text_rect)

    def _convert_move_to_direction(self, move: int):
        """`move` - 0 - left, 1 - straight, 2 - right"""
        move -= 1
        direction = self.snake.direction.value
        direction += move + 4
        direction %= 4
        return c.Direction(direction)

    def play_step(self, direction: c.Direction) -> Tuple[int, bool, int]:
        reward = 0
        game_over = False
        self.snake.direction = direction
        self.screen.fill(c.BACKGROUND_COLOR)
        self.snake.update()
        if self.snake.check_for_collision():
            reward = -100
            game_over = True
        self._print_points()
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        if self.snake.has_eaten(self.apple):
            print("Reward:", reward)
            reward = 10
            self.points += 1
        pygame.display.update()
        self.clock.tick(c.FPS)
        
        return reward, game_over, self.points


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
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            
            _, game_over, _ = self.play_step(direction)
            if game_over:
                break