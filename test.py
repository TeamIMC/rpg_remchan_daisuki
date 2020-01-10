# IMC_RPG_ENGINE
# Copyright (C) 2019, United IMC

from backend import *

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
#screen.fill((0, 0, 0))
screen.fill((55, 55, 55))
pygame.display.set_caption('IMC RPG')
clock = pygame.time.Clock()

test = rpg_map("test")
testchr = character("test")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    mapsurf = resize(testchr.get_surf(), 3)
    screen.blit(mapsurf, (0, 0))
    pygame.display.flip()