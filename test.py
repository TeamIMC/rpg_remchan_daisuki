# IMC_RPG_ENGINE
# Copyright (C) 2019, Wonjun Jung
#

import pygame
import os
import sys
import json

class InvalidFileException(Exception):
	pass

class texture:
	def __init__(self, image):
		if not image.get_width() == 16 and image.get_height() == 16:
			raise InvalidFileException("Not a valid Texture File")

		self.image = image
		self.width = image.get_width() / 32
		self.height = image.get_height() / 32

	def get(self, num):
		# TODO: 초기화시에 미리 다 잘라둘것
		if num >= self.width * self.height:
			raise IndexError("Texture index out of range")

		srcrect = pygame.Rect(int(num % self.width) * 32, int(num / self.width) * 32, 32, 32)

		rtnsurf = pygame.Surface((32, 32))
		rtnsurf.blit(self.image, (0, 0), srcrect)

		return rtnsurf

class map:
	def __init__(self, name):
		self.texture = texture(pygame.image.load(os.path.join("maps", name, "texture.png")).convert_alpha())
		# TODO: BMP 파싱 도무지 못해먹겠으니 알아서 구현할것. 임시로 텍스트 파싱으로 가져다둠
		self.floor = json.load(open(os.path.join("maps", name, "floor")))
		print(self.floor)

	def get_surf(self):
		height = len(self.floor)
		width = len(self.floor[0])
		rtnsurf = pygame.Surface((width * 32, height * 32))

		for y in range(height):
			for x in range(width):
				texturenumb = int.from_bytes(bytearray.fromhex(self.floor[y][x][:2]), sys.byteorder)
				rtnsurf.blit(self.texture.get(texturenumb), (x * 32, y * 32))

		return rtnsurf

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
pygame.display.set_caption('IMC RPG')
clock = pygame.time.Clock()

test = map("test")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(test.get_surf(), (0, 0))
    pygame.display.update()