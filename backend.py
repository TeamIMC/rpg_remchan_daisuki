# IMC_RPG_ENGINE
# Copyright (C) 2019, United IMC

import pygame
import os
import sys
import json

# TODO: 예외 클래스 따로 생성해둘것

#####################
##### Functions #####
#####################

def resize(surf, size):
    # 각각 길이에 size인수 값 곱해서 스케일 후 리턴
    return pygame.transform.scale(surf, tuple(map(lambda x: int(x*size), surf.get_size())))

def get_texture(image, tile_size = (32, 32), texture_size = (512, 512)):
    # 텍스쳐 파일 사이즈가 맞는지 확인
    if not image.get_size() == texture_size:
        raise Exception("Not a valid Texture File")
    # 이미지 크기 타일단위로 변환
    width = int(image.get_width() / tile_size[0])
    height = int(image.get_height() / tile_size[1])
    # 사이즈 타일단위로 잘라서 리턴
    rtnlist = []
    for x in range(width * height):
        # 타일 위치 지정하는 Rect 생성
        # 시작 지점 = (x % 가로타일개수 * 타일 길이, x / 가로타일개수 * 타일 길이)
        srcrect = pygame.Rect(int(x % width) * tile_size[0], int(x / width) * tile_size[1], tile_size[0], tile_size[1])
        rtnlist.append(image.subsurface(srcrect))
    return tuple(rtnlist)

def merge_hitbox(hitboxes):
    rtnlist = hitboxes[0]
    for hitbox in hitboxes[1:]:
        for y in range(len(rtnlist)):
            for x in range(len(rtnlist[0])):
                if hitbox[y][x]:
                    rtnlist[y][x] = 1
    return rtnlist
#####################
###### Classes ######
#####################

class rpg_map:
    def __init__(self, name):
        ### 데이터 로딩 ###
        self.texture = get_texture(pygame.image.load(os.path.join("maps", name, "texture.png")).convert_alpha())
        # TODO: BMP 파싱 도무지 못해먹겠으니 알아서 구현할것. 임시로 텍스트 파싱으로 가져다둠
        self.floor = json.load(open(os.path.join("maps", name, "floor")))
        self.object = json.load(open(os.path.join("maps", name, "object")))
        ### 맵 Surface 생성 ###
        # floor 파일에서 맵 사이즈 구해오기. 단, 맵은 직사각형이어야 함
        height = len(self.floor)
        width = len(self.floor[0])
        # Surface 생성 후 타일별로 그려서 리턴
        self.mapsurf = pygame.Surface((width * 32, height * 32), flags = pygame.SRCALPHA)
        for y in range(height):
            for x in range(width):
                # 색상코드 앞 2자리 받아서 바이트로 변환후 int로 재변환
                floornumb = int.from_bytes(bytearray.fromhex(self.floor[y][x][:2]), sys.byteorder)
                objectnumb = int.from_bytes(bytearray.fromhex(self.object[y][x][:2]), sys.byteorder)
                self.mapsurf.blit(self.texture[floornumb], (x * 32, y * 32))
                self.mapsurf.blit(self.texture[objectnumb], (x * 32, y * 32))

        ### 맵 충돌 포인트 생성 ###
        self.hitbox = tuple(map(lambda x:  map(lambda y:  int(y[2:4]), x), self.object))

    #def get_surf(self, )

class character:
    def __init__(self, name):
        self.texture = get_texture(pygame.image.load(os.path.join("characters", name + ".png")).convert_alpha(), texture_size = (96, 128))
        self.loc = (0, 0)
        self.direction = 0
        self.foot = 1
        self.is_moving = False
    
    def get_hitbox(self, size):
        # 히트박스 사이즈에 맞는 빈 리스트 생성
        # 출처: How to create empty list by length
        # https://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size
        hitbox = [[0] * size[0]] * size[1]
        hitbox[self.loc[1]][self.loc[0]] = 1
        if is_moving:
            if self.direction == 0:
                hitbox[self.loc[1] + 1][self.loc[0]] = 1
            elif self.direction == 1:
                hitbox[self.loc[1]][self.loc[0] - 1] = 1
            elif self.direction == 2:
                hitbox[self.loc[1]][self.loc[0] + 1] = 1
            elif self.direction == 3:
                hitbox[self.loc[1] - 1][self.loc[0]] = 1
        return hitbox


    def add_move_queue(self, direction, hitbox, duration = 1, fps = 60, tile_size = 32):
        # direction 0 = 아래 1 = 왼쪽 2 = 오른쪽 3 = 위쪽
        if direction == 0:
            if self.loc[1] == len(hitbox) - 1:
                return 1
            elif hitbox[self.loc[1] + 1][self.loc[0]]:
                return 1
        elif direction == 1:
            if self.loc[0] == 0:
                return 1
            elif hitbox[self.loc[1]][self.loc[0] - 1]:
                return 1
        elif direction == 2:
            if self.loc[0] == len(hitbox[0]) - 1:
                return 1
            elif hitbox[self.loc[1]][self.loc[0] + 1]:
                return 1
        elif direction == 3:
            if self.loc[1] == 0:
                return 1
            elif hitbox[self.loc[1] - 1][self.loc[0]]:
                return 1
        self.direction = direction
        self.speed = tile_size / (fps * duration)
        self.count = fps * duration
        # 발 바꾸기
        self.foot = int(not self.foot)
        self.is_moving = True
        return 0

    #def run_queue(self, surf, ):

    def texture_test(self):
        rtnsurf = pygame.Surface((96, 128), flags = pygame.SRCALPHA)
        for y in range(4):
            for x in range(3):
                texturenumb = y * 3 + x
                rtnsurf.blit(self.texture[texturenumb], (x * 32, y * 32))
        return rtnsurf 