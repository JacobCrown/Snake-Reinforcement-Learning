import pygame


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((400, 500))
    pygame.display.set_caption('Snake Reinforcement Learning')
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False