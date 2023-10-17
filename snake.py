from collections import namedtuple
from typing import Optional

import pygame

from constants import Direction, WINDOW_HEIGHT, WINDOW_WIDTH, BLOCK_SIZE, SNAKE_COLOR

Point = namedtuple("Point", ("x", "y"))


class Snake():
    def __init__(self):
        self.direction = Direction.UP
        half_w, half_h = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.points = [Point(half_w, half_h), Point(half_w - BLOCK_SIZE, half_h),
                       Point(half_w - 2*BLOCK_SIZE, half_h)]
        self.speed = BLOCK_SIZE

    def update(self) -> None:
        self.points.pop()
        point = self._move_snake()
        
        self.points.insert(0, point)

    def _move_snake(self) -> Point:
        point: Optional[Point] = None
        head = self.points[0]
        if self.direction == Direction.UP:
            point = Point(head.x, head.y - self.speed)
        if self.direction == Direction.DOWN:
            point = Point(head.x, head.y + self.speed)
        if self.direction == Direction.LEFT:
            point = Point(head.x - self.speed, head.y)
        if self.direction == Direction.RIGHT:
            point = Point(head.x + self.speed, head.y)
        
        assert point is not None, f"Point object cannot be none"
        return point

    def draw(self, surf: pygame.Surface):
        for p in self.points:
            pygame.draw.rect(surf, SNAKE_COLOR, (p.x, p.y, BLOCK_SIZE, BLOCK_SIZE), 2)
            
    def check_for_collision(self) -> bool:
        head = self.points[0]
        x, y = head.x, head.y
        if x < 0 or x >= WINDOW_WIDTH:
            return True
        elif y < 0 or y >= WINDOW_HEIGHT:
            return True
        
        # check if snake touches itself
        for p in self.points[1:]:
            if x == p.x and y == p.y:
                return True

        return False
