# IMC_RPG_ENGINE
# Copyright (C) 2019, United IMC

# 경고: 여기에 쓰인 코드는 예시용으로 작성된 코드이며, 실제 게임에 들어갈때는 코드가 달라질 수 있음.
from backend import *
from pygame.locals import *

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
# screen.fill((0, 0, 0))
screen.fill((55, 55, 55))
pygame.display.set_caption('IMC RPG')
clock = pygame.time.Clock()
fps = 60

test = rpg_map("test")
testchr = character("test")

keypress = False
key = None
duration = 0.5
while True:
    hitbox = merge_hitbox((test.get_hitbox(), testchr.get_hitbox((len(test.hitbox[0]), len(test.hitbox)))))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (K_w, K_a, K_s, K_d):
                keypress = True
                key = event.key
                direction = {K_w: 3, K_a: 1, K_s: 0, K_d: 2}[event.key]
            if event.mod & KMOD_SHIFT:
                duration = 0.25
            else:
                duration = 0.5
        elif event.type == pygame.KEYUP:
            if event.key == key:
                keypress = False
    if keypress:
        if not testchr.is_moving:
            testchr.add_move_queue(direction, hitbox, duration = duration, fps = fps)

    mapsurf = test.mapsurf.copy()
    testchr.run_queue(mapsurf), (0, 0)

    mapsurf = resize(mapsurf, 3)
    screen.blit(mapsurf, (0, 0))
    pygame.display.flip()
    print(clock.get_fps())
    clock.tick(fps)