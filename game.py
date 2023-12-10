import os
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
        if c.SHOW_GAME:
            pygame.init()
            pygame.display.set_caption('Snake Reinforcement Learning')

            self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT + 100))
            self.board = pygame.Surface((c.BOARD_WIDTH, c.BOARD_HEIGHT))
            
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font("freesansbold.ttf", 32)
            os.environ['SDL_VIDEO_WINDOW_POS'] = "2500,200"
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

    def fix_move_to_legal_move(self, move):
        """`move` - 0 - left, 1 - right, 2 - up, 3 - down"""
        assert move >= 0 and move <= 3, f"Move `{move}` has to be an integer between 0 and 3"
        if move == 0 and self.snake.direction == c.Direction.RIGHT:
            move = 1
        elif move == 1 and self.snake.direction == c.Direction.LEFT:
            move = 0
        elif move == 2 and self.snake.direction == c.Direction.DOWN:
            move = 3
        elif move == 3 and self.snake.direction == c.Direction.UP:
            move = 2
        return c.Direction(move)

    def _update_screen_with_borders(self):
        self.screen.fill(c.BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, c.BORDER_COLOR, (0, 100,
                        c.WINDOW_WIDTH, c.WINDOW_HEIGHT), c.BLOCK_SIZE)
        self.screen.blit(self.board, (c.BLOCK_SIZE, 100 + c.BLOCK_SIZE))
        self._print_points()

    def update_screen(self):
        self.board.fill(c.BACKGROUND_COLOR)
        self.apple.draw(self.board)
        self.snake.draw(self.board)
        self._update_screen_with_borders()
        pygame.display.update()
        self.clock.tick(c.FPS)

    def play_step(self, direction: c.Direction) -> Tuple[int, bool, int]:
        reward = -1
        game_over = False

        self.snake.update(direction)
        if c.SHOW_GAME:
            self.update_screen()

        if self.snake.check_for_collision():
            reward = -30
            game_over = True
            print("COLLISION ...")

        if self.snake.total_moves > self.stale_moves_threshold:
            reward = -30
            game_over = True
            print("STAGNATION ...")
            
        if self.snake_has_eaten():
            reward = 30
            self.points += 1

        return reward, game_over, self.points

    def _draw_apple_coordinates(self):
        self.apple.x = random.randrange(0, c.BOARD_BLOCK_WIDTH)
        self.apple.y = random.randrange(0, c.BOARD_BLOCK_HEIGHT)


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

    def get_board_pixels(self) -> np.ndarray:
        """Method for obtaining pixel values from board in CxHxW format"""
        arr = np.zeros((3, c.BOARD_BLOCK_HEIGHT, c.BOARD_BLOCK_WIDTH)) \
                                                                .astype("uint8")

        # draw walls
        arr = np.array([np.pad(arr[i], 1, constant_values=color) for i, color in
                        enumerate(c.BORDER_COLOR)])

        # draw snake
        arr[:,self.snake.head.y // c.BLOCK_SIZE + 1, self.snake.head.x // c.BLOCK_SIZE + 1] \
                                                                    = c.HEAD_COLOR
        for p in self.snake.points[1:]:
            arr[:,p.y // c.BLOCK_SIZE + 1, p.x // c.BLOCK_SIZE + 1] = c.SNAKE_COLOR

        # draw apple
        arr[:,self.apple.y // c.BLOCK_SIZE + 1, self.apple.x // c.BLOCK_SIZE + 1] = c.APPLE_COLOR

        return arr

    def obtain_game_as_np_array(self):
        arr = np.zeros((c.BOARD_BLOCK_HEIGHT, c.BOARD_BLOCK_WIDTH))


        try:
            # draw snake
            arr[self.snake.head.y, self.snake.head.x] = 2
            for p in self.snake.points[1:]:
                arr[p.y, p.x] = 1

            # draw apple
            arr[self.apple.y, self.apple.x] = 9
        except IndexError as e:
            return

        print("BOARD ARRAY: ")
        print(arr)
        print()

        return arr
        

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