import pygame
import os
import sys
import json

## TODO: 예외 클래스 따로 생성해둘것

# get_texture 함수로 대체함. 레퍼런스용으로 남겨둠. __init__ 함수는 미완성임
"""
class texture:
	def __init__(self, image):
		self.image = image
		self.width = image.get_width() / 32
		self.height = image.get_height() / 32

		# 이미지 정상인지 체크
		if not self.width == 16 and self.height == 16:
			raise Exception("Not a valid Texture File")


	def get(self, num):
		# TODO: 초기화시에 미리 다 잘라둘것
		if num >= self.width * self.height:
			raise IndexError("Texture index out of range")

		srcrect = pygame.Rect(int(num % self.width) * 32, int(num / self.width) * 32, 32, 32)

		rtnsurf = pygame.Surface((32, 32))
		rtnsurf.blit(self.image, (0, 0), srcrect)

		return rtnsurf
"""

def get_texture(image):
	# 이미지 크기 타일단위로 변환
	width = image.get_width() / 32
	height = image.get_height() / 32
	# 텍스쳐 파일이 맞는지 확인
	if not width == 16 and height == 16:
		raise Exception("Not a valid Texture File")
	# 타일단위로 잘라서 리턴
	rtnlist = []
	for x in range(256):
		srcrect = (int(x % 16) * 32, int(x / 16) * 32, 32, 32)
		surf = pygame.Surface((32, 32)).convert_alpha()
		surf.blit(image, (0, 0), srcrect)
		rtnlist.append(surf)
	return tuple(rtnlist)

class map:
	def __init__(self, name):
		self.texture = get_texture(pygame.image.load(os.path.join("maps", name, "texture.png")).convert_alpha())
		# TODO: BMP 파싱 도무지 못해먹겠으니 알아서 구현할것. 임시로 텍스트 파싱으로 가져다둠
		self.floor = json.load(open(os.path.join("maps", name, "floor")))
		print(self.floor)

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