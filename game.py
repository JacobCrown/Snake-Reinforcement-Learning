import random
import sys
from typing import Tuple

import numpy as np
import pygame

import constants as c
from snake import Snake
from apple import Apple


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Snake Reinforcement Learning')

        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.stale_moves_threshold = 150
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.apple = Apple()
        self.reset_apple()
        self.points = 0

    def _print_points(self):
        text = self.font.render(f"Score: {self.points}",
                                True, c.TEXT_COLOR, c.BACKGROUND_COLOR)
        text_rect = text.get_rect()
        
        text_rect.topright = (c.WINDOW_WIDTH - 50, 10)
        self.screen.blit(text, text_rect)

    def _change_direction_from_int(self, move: int):
        dir = self.snake.direction
        value: int
        if move < 0:
            value = 3 if dir.value == 0 else dir.value + move
        elif move > 0:
            value = 0 if dir.value == 3 else dir.value + move
        else:
            value = dir.value
        return c.Direction(value)

    def convert_move_to_direction(self, move: int):
        """`move` - 0 - left, 1 - straight, 2 - right"""
        move -= 1
        direction = self._change_direction_from_int(move)
        return direction

    def update_screen(self, direction: c.Direction):
        self.snake.direction = direction
        self.screen.fill(c.BACKGROUND_COLOR)
        self.snake.update()
        self._print_points()
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)

    def play_step(self, direction: c.Direction) -> Tuple[np.ndarray, int, bool, int]:
        reward = 0
        game_over = False

        self.update_screen(direction)

        if self.snake.check_for_collision():
            reward = -10
            game_over = True

        if self.snake.total_moves > self.stale_moves_threshold:
            reward = -10
            game_over = True
            
        if self.snake_has_eaten():
            reward = 10
            self.points += 1

        pygame.display.update()
        self.clock.tick(c.FPS)
        
        return self.get_current_state(), reward, game_over, self.points

    def get_current_state(self):
        head = self.snake.head
        point_l = c.Point(head.x - 20, head.y)
        point_r = c.Point(head.x + 20, head.y)
        point_u = c.Point(head.x, head.y - 20)
        point_d = c.Point(head.x, head.y + 20)
        
        dir_l = self.snake.direction == c.Direction.LEFT
        dir_r = self.snake.direction == c.Direction.RIGHT
        dir_u = self.snake.direction == c.Direction.UP
        dir_d = self.snake.direction == c.Direction.DOWN

        state = [
            # Danger up
            self.snake.is_collision(point_u),

            # Danger down
            self.snake.is_collision(point_d),

            # Danger right
            self.snake.is_collision(point_r),

            # Danger left
            self.snake.is_collision(point_l),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            self.apple.x < head.x,  # food left
            self.apple.x > head.x,  # food right
            self.apple.y < head.y,  # food up
            self.apple.y > head.y  # food down
            ]

        return np.array(state, dtype=np.float32)

    def _draw_apple_coordinates(self):
        self.apple.x = random.randrange(0, c.WINDOW_WIDTH-1, c.BLOCK_SIZE)
        self.apple.y = random.randrange(0, c.WINDOW_HEIGHT-1, c.BLOCK_SIZE)

    def reset_apple(self):
        self._draw_apple_coordinates()
        if self.snake is not None:
            while any((self.apple.x == x and self.apple.y == y) 
                      for x, y in self.snake.points):
                self._draw_apple_coordinates()

    def snake_has_eaten(self):
        if self.apple.x == self.snake.head.x and self.apple.y == self.snake.head.y:
            self.snake.grow()
            self.snake.total_moves = 0
            self.reset_apple()
            return True
        return False

    def main_loop(self):
        """Used for single-player game"""
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
            
            _, _, game_over, _ = self.play_step(direction)
            if game_over:
                break