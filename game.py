# Team IMC - RPG Project.

# Current Version : 1.0

import pygame

pygame.init()
size=[1920,1080]
screen=pygame.display.set_mode(size)
pygame.display.set_caption('IMC RPG')
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    screen.fill((0,0,0))
    pygame.display.flip()