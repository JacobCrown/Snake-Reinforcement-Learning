import random
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

        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT + 100))
        self.board = pygame.Surface((c.BOARD_WIDTH, c.BOARD_HEIGHT))
        
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

    def _update_screen_with_borders(self):
        self.screen.fill(c.BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, c.BORDER_COLOR, (0, 100,
                        c.WINDOW_WIDTH, c.WINDOW_HEIGHT), c.BLOCK_SIZE)
        self.screen.blit(self.board, (c.BLOCK_SIZE, 100 + c.BLOCK_SIZE))
        self._print_points()

    def update_screen(self, direction: c.Direction):
        self.snake.direction = direction
        self.board.fill(c.BACKGROUND_COLOR)
        self.snake.update(direction)
        self.apple.draw(self.board)
        self.snake.draw(self.board)
        self._update_screen_with_borders()

    def play_step(self, direction: c.Direction) -> Tuple[int, bool, int]:
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
        
        return reward, game_over, self.points

    def _draw_apple_coordinates(self):
        self.apple.x = random.randrange(0, c.BOARD_WIDTH-1, c.BLOCK_SIZE)
        self.apple.y = random.randrange(0, c.BOARD_HEIGHT-1, c.BLOCK_SIZE)

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
            
            _, game_over, _ = self.play_step(direction)
            if game_over:
                break