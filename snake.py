from typing import Optional

import pygame

from constants import Direction, BOARD_BLOCK_HEIGHT, BOARD_BLOCK_WIDTH, BLOCK_SIZE, SNAKE_COLOR, \
                      Point, HEAD_COLOR


class Snake():
    def __init__(self):
        self.direction = Direction.RIGHT
        half_w, half_h = BOARD_BLOCK_WIDTH // 2, BOARD_BLOCK_HEIGHT // 2
        self.points = [Point(half_w, half_h), Point(half_w - 1, half_h),
                       Point(half_w - 2, half_h)]
        self.speed = 1
        self.head = self.points[0]
        self.total_moves = 0

    def update(self, direction: Direction) -> None:
        self.direction = direction
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
        self.total_moves += 1
        return point

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, HEAD_COLOR, (self.head.x * BLOCK_SIZE, self.head.y * BLOCK_SIZE,
                                             BLOCK_SIZE, BLOCK_SIZE))
        for p in self.points[1:]:
            pygame.draw.rect(surf, SNAKE_COLOR, (p.x * BLOCK_SIZE, p.y * BLOCK_SIZE,
                                                 BLOCK_SIZE, BLOCK_SIZE))

    def _check_collision_with_walls(self, x: int, y: int) -> bool:
        if x < 0 or x >= BOARD_BLOCK_WIDTH:
            return True
        elif y < 0 or y >= BOARD_BLOCK_HEIGHT:
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

    def grow(self):
        # simply append new point at the end, since last point is just popped
        self.points.append(Point(x=1, y=1))
