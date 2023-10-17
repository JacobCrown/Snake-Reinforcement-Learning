import pygame

import constants as c

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Reinforcement Learning')
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False