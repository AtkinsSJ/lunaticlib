import pygame
from tile import Tile

class LevelTile:
	"""A tile in a level"""
	
	def __init__(self, floor, wall, lighting, item):
		self.floor = floor
		self.wall = wall
		self.lighting = lighting
		self.lightColour = self.set_lighting_color(lighting)
		self.item = item
	
	def set_lighting_color(self, lighting):
		if lighting == 128:
			#No lighting
			return pygame.Color(0,0,0,0)
		elif lighting > 128:
			#Bright
			return pygame.Color(255, 255, 255, (lighting-128)*2)
		else:
			#Dark
			return pygame.Color(255, 255, 255, 255-(lighting*2))
	
	def draw(self):
		surface = pygame.Surface( (32, 48), pygame.SRCALPHA )
		# Draw the wall if there is one
		if self.wall:
			surface.blit(self.floor.draw(), (0,0))
			surface.blit(self.wall.draw(), (0,24))
		else:
			# Draw the floor
			surface.blit(self.floor.draw(), (0,24))
		# TODO: DRAW THE ITEM HERE
		# Add lighting
		#surface.fill(self.lightColour)
		return surface
		
