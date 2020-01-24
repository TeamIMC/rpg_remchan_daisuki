# IMC_RPG_ENGINE
# Copyright (C) 2019, United IMC

# 경고: 여기에 쓰인 코드는 예시용으로 작성된 코드이며, 실제 게임에 들어갈때는 코드가 달라질 수 있음.
import pygame
from backend import *
from pygame.locals import *
from os.path import abspath, dirname

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
# screen.fill((0, 0, 0))
screen.fill((55, 55, 55))
pygame.display.set_caption('IMC RPG')
clock = pygame.time.Clock()
fps = 60

basepath = dirname(abspath(__file__))

test = rpgMap("test", basepath)
testchr = character("test", basepath)

keypress = False
key = None
duration = 1

while True:
    hitbox = merge_hitbox((test.get_hitbox(), testchr.get_hitbox((len(test.get_hitbox()[0]), len(test.get_hitbox())))))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (K_w, K_a, K_s, K_d):
                keypress = True
                key = event.key
                direction = {K_w: (0, -1), K_a: (-1, 0), K_s: (0, 1), K_d: (1, 0)}[event.key]
            if event.mod & KMOD_SHIFT:
                duration = 0.25
            else:
                duration = 0.5
        elif event.type == pygame.KEYUP:
            if event.key == key:
                keypress = False
    if keypress:
        testchr.add_move_queue(direction, hitbox, duration, fps)

    mapsurf = test.get_surf()
    testchr.run_queue(mapsurf)

    mapsurf = resize(mapsurf, 3)
    screen.blit(mapsurf, (0, 0))
    pygame.display.flip()
    clock.tick(fps)
