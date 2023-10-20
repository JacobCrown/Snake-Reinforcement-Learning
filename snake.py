from typing import Optional

import pygame

from apple import Apple
from constants import Direction, WINDOW_HEIGHT, WINDOW_WIDTH, BLOCK_SIZE, SNAKE_COLOR, \
                      Point


class Snake():
    def __init__(self):
        self.direction = Direction.RIGHT
        half_w, half_h = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.points = [Point(half_w, half_h), Point(half_w - BLOCK_SIZE, half_h),
                       Point(half_w - 2*BLOCK_SIZE, half_h)]
        self.speed = BLOCK_SIZE
        self.head = self.points[0]

    def update(self) -> None:
        self.points.pop()
        point = self._move_snake()
        
        self.points.insert(0, point)
        self.head = point

    def _move_snake(self) -> Point:
        point: Optional[Point] = None
        self.head = self.points[0]
        if self.direction == Direction.UP:
            point = Point(self.head.x, self.head.y - self.speed)
        elif self.direction == Direction.DOWN:
            point = Point(self.head.x, self.head.y + self.speed)
        elif self.direction == Direction.LEFT:
            point = Point(self.head.x - self.speed, self.head.y)
        else:
            point = Point(self.head.x + self.speed, self.head.y)
        
        assert point is not None, f"Point object cannot be none"
        return point

    def draw(self, surf: pygame.Surface):
        for p in self.points:
            pygame.draw.rect(surf, SNAKE_COLOR, (p.x, p.y, BLOCK_SIZE, BLOCK_SIZE), 2)

    def _check_collision_with_walls(self, x: int, y: int) -> bool:
        if x < 0 or x >= WINDOW_WIDTH:
            return True
        elif y < 0 or y >= WINDOW_HEIGHT:
            return True
        return False

    def _check_collision_with_tail(self, x, y) -> bool:
        for p in self.points[1:]:
            if x == p.x and y == p.y:
                return True
        return False

    def _check_collision(self, x, y) -> bool:
        if self._check_collision_with_walls(x, y):
            return True
        if self._check_collision_with_tail(x, y):
            return True
        return False

    def is_collision(self, point: Point) -> bool:
        return self._check_collision(point.x, point.y)
            
    def check_for_collision(self) -> bool:
        x, y = self.head.x, self.head.y
        return self._check_collision(x, y)

    def _grow(self):
        # simply append new point at the end, since last point is just popped
        self.points.append(Point(x=1, y=1))

    def has_eaten(self, apple: Apple) -> bool:
        if apple.x == self.head.x and apple.y == self.head.y:
            self._grow()
            apple.reset_apple()
            return True
        return False