# IMC_RPG_ENGINE
# Copyright (C) 2019, United IMC

import pygame
import os
import sys
import json

# TODO: 예외 클래스 따로 생성해둘것

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
        surf = pygame.Surface(tile_size).convert_alpha()
        surf.blit(image, (0, 0), srcrect)
        rtnlist.append(surf)
    return tuple(rtnlist)

class rpg_map:
    def __init__(self, name):
        self.texture = get_texture(pygame.image.load(os.path.join("maps", name, "texture.png")).convert_alpha())
        # TODO: BMP 파싱 도무지 못해먹겠으니 알아서 구현할것. 임시로 텍스트 파싱으로 가져다둠
        self.floor = json.load(open(os.path.join("maps", name, "floor")))
        self.object = json.load(open(os.path.join("maps", name, "object")))

    def get_surf(self):
        # floor 파일에서 맵 사이즈 구해오기. 단, 맵은 직사각형이어야 함
        height = len(self.floor)
        width = len(self.floor[0])
        # Surface 생성 후 타일별로 그려서 리턴
        rtnsurf = pygame.Surface((width * 32, height * 32)).convert_alpha()
        for y in range(height):
            for x in range(width):
                texturenumb = int.from_bytes(bytearray.fromhex(self.floor[y][x][:2]), sys.byteorder)
                rtnsurf.blit(self.texture[texturenumb], (x * 32, y * 32))
        return rtnsurf

class character:
    def __init__(self, name):
        self.texture = get_texture(pygame.image.load(os.path.join("characters", name + ".png")).convert_alpha(), texture_size = (96, 128))
    def get_surf(self):
        rtnsurf = pygame.Surface((96, 128)).convert_alpha()
        for y in range(4):
            for x in range(3):
                texturenumb = y * 3 + x
                rtnsurf.blit(self.texture[texturenumb], (x * 32, y * 32))
        return rtnsurf