# IMC_RPG_ENGINE
# Copyright (C) 2019, United IMC

import pygame
import os
import sys
import json
import copy
from pygame.image import load as load_image
from os.path import join

# TODO: 예외 클래스 따로 생성해둘것

#####################
##### Functions #####
#####################

def resize(surf, size):
    # 각각 길이에 size인수 값 곱해서 스케일 후 리턴
    return pygame.transform.scale(surf, [x * size for x in surf.get_size()])

def get_texture(path, tile_size, texture_size):
    image = load_image(path).convert_alpha()

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
        srcrect = pygame.Rect((int(x % width) * tile_size[0], int(x / width) * tile_size[1]), tile_size)
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

def hex2int(hex):
    return int.from_bytes(bytearray.fromhex(hex), sys.byteorder)

#####################
###### Classes ######
#####################

class rpgMap:
    def __init__(self, name, basepath, tile_size = (32, 32), texture_size = (512, 512)):
        # 경로 저장
        self.path = join(basepath, "maps", name)

        self.tile_size = tile_size
        self.texture_size = texture_size

        self.load_data()
        self.generate_surf()

    def load_data(self):
        ### 데이터 로딩 ###
        self.floor_texture = get_texture(join(self.path, "texture.png"), self.tile_size, self.texture_size)
        self.object_texture = get_texture(join(self.path, "object.png"), self.tile_size, self.texture_size)
        # TODO: BMP 파싱 도무지 못해먹겠으니 알아서 구현할것. 임시로 텍스트 파싱으로 가져다둠
        self.floor = json.load(open(join(self.path, "floor")))
        self.object = json.load(open(join(self.path, "object")))

        self.info = json.load(open(join(self.path, "info.json")))

    def get_hitbox(self):
        return [[hex2int(y[2:4]) for y in x] for x in self.object]

    def generate_surf(self):
        # floor 파일에서 맵 사이즈 구해오기. 단, 맵은 직사각형이어야 함
        height = len(self.floor)
        width = len(self.floor[0])
        # Surface 생성 후 타일별로 그려서 리턴
        self.mapsurf = pygame.Surface((width * 32, height * 32), flags = pygame.SRCALPHA)
        for y in range(height):
            for x in range(width):
                # 색상코드 앞 2자리 받아서 바이트로 변환후 int로 재변환
                floornumb = hex2int(self.floor[y][x][:2])
                objectnumb = hex2int(self.object[y][x][:2])
                self.mapsurf.blit(self.floor_texture[floornumb], (x * 32, y * 32))
                self.mapsurf.blit(self.object_texture[objectnumb], (x * 32, y * 32))

    def get_surf(self):
        return self.mapsurf.copy()

class character:
    def __init__(self, name, path):
        self.texture = get_texture(join(path, "characters", name + ".png"), texture_size = (96, 128), tile_size = (32, 32))
        self.loc = [0, 0]
        self.pixel = [0, 0]
        self.direction = [0, 0]
        self.count = 0
        self.count_orig = 0
        self.foot = 0
        self.foot_count = 0
        self.is_moving = False

    def get_texture(self, direction, foot):
        # direction 0 = 아래 1 = 왼쪽 2 = 오른쪽 3 = 위쪽
        # foot 0 = 왼발 1 = 차렷 2 = 오른발
        if direction == (0, 1):
            direction = 0
        elif direction == (-1, 0):
            direction = 1
        elif direction == (1, 0):
            direction = 2
        elif direction == (0, -1):
            direction = 3
        else:
            direction = 0

        return self.texture[direction * 3 + foot]

    def get_hitbox(self, size):
        # 히트박스 사이즈에 맞는 빈 리스트 생성
        # 출처: How to create empty list by length
        # https://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size
        hitbox = [[0 for y in range(size[0])] for x in range(size[1])]
        hitbox[self.loc[1]][self.loc[0]] = 2
        if self.is_moving:
            hitbox[self.loc[1] + self.direction[1]][self.loc[0] + self.direction[0]] = 1
        return hitbox

    def add_move_queue(self, direction, hitbox, duration = 1, fps = 60, tile_size = 32):
        # direction 0 = 아래 1 = 왼쪽 2 = 오른쪽 3 = 위쪽
        # 캐릭터가 움직이는지, 해당 위치에 뭐가 있지는 않은지 확인
        if self.is_moving:
            return 1
        else:
            # 움직이지 못하는 곳으로 가려 했을때도 바라보는 방향은 바뀌도록 검사 전에 바꿈
            self.direction = direction
            temploc = [x + y for x, y in zip(self.loc, direction)]
            if temploc[0] > len(hitbox[0]) - 1 or temploc[1] > len(hitbox) - 1 or temploc[0] < 0 or temploc[1] < 0:
                return 2
            elif hitbox[temploc[1]][temploc[0]]:
                return 3
        #방향, 속도, 움직일 횟수, 발, 움직이는지 여부 바꾸기
        self.speed = tile_size / (fps * duration)
        self.count = fps * duration
        self.count_orig = self.count
        self.foot = 0
        self.foot_count = self.count - self.count / 4
        self.is_moving = True
        return 0

    def run_queue(self, surf, tile_size = 32):
        if self.is_moving:
            if self.count == 0:
                # 카운트가 0에 도달했을 경우, 내부적으로 처리되는 위치를 옮기고 픽셀 위치 역시
                # 해당 위치로 이동시킨 뒤 is_moving을 False로 바꿈
                self.is_moving = False
                self.loc = [x + y for x, y in zip(self.loc, self.direction)]
                self.pixel = [x * tile_size for x in self.loc]
                self.is_moving = False
            else:
                # direction에 따라 픽셀을 speed만큼 이동시킨 뒤 카운트 감소
                if self.count <= self.foot_count:
                    self.foot_count -= self.count_orig / 4
                    if self.foot == 2:
                        self.foot = 1
                    else:
                        self.foot += 1
                self.pixel[0] += self.direction[0] * self.speed
                self.pixel[1] += self.direction[1] * self.speed
                self.count -= 1
            surf.blit(self.get_texture(self.direction, self.foot), self.pixel)
        else:
            surf.blit(self.get_texture(self.direction, 1), self.pixel)
        return

    def texture_test(self):
        rtnsurf = pygame.Surface((96, 128), flags = pygame.SRCALPHA)
        for y in range(4):
            for x in range(3):
                texturenumb = y * 3 + x
                rtnsurf.blit(self.texture[texturenumb], (x * 32, y * 32))
        return rtnsurf
