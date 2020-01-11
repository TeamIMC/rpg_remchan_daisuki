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

test = rpg_map("test_doyun")
testchr = character("miku1")

##############################
##    Player Walk Script    ##
##############################
x = 1
y = 1
mode2 = 0
def move(mod) :
    global x, y, mode2
    mode2 = mod
    if mod == 1 :
        y = y + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[1], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        y = y + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[0], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        y = y + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[2], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        y = y + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[0], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
    elif mod == 2 :
        y = y - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[9], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        y = y - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[10], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        y = y - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[11], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        y = y - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[10], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
    elif mod == 3 :
        x = x + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[7], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        x = x + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[6], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        x = x + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[7], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        x = x + 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[8], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
    elif mod == 4 :
        x = x - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[3], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        x = x - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[4], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        x = x - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[5], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
        x = x - 1/4
        screen.blit(test.mapsurf, (0, 0))
        screen.blit(testchr.texture[4], (32*x-32,32*y-32))
        pygame.time.wait(50)
        pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                move(1)
            elif event.key == pygame.K_UP:
                move(2)
            elif event.key == pygame.K_RIGHT:
                move(3)
            elif event.key == pygame.K_LEFT:
                move(4)
            else:
                pass
    mapsurf = resize(testchr.texture_test(), 3)
    screen.blit(test.mapsurf, (0, 0))
    if mode2 == 1 :
        screen.blit(testchr.texture[1], ((x-1)*32,(y-1)*32))
    elif mode2 == 2 :
        screen.blit(testchr.texture[10], ((x-1)*32,(y-1)*32))
    elif mode2 == 3 :
        screen.blit(testchr.texture[7], ((x-1)*32,(y-1)*32))
    elif mode2 == 4 :
        screen.blit(testchr.texture[4], ((x-1)*32,(y-1)*32))
    else:
       pass
    pygame.display.flip()