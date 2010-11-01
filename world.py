import string
import pygame
from pygame.locals import *
from tile import Tile
from level import Level
import palette
from functions import *

class World:
	"""Holds an entire world - the levels, tiles, and metadata"""
	
	def __init__(self, filename, screen):
		"""Load DLW file and extract useful data"""
		self.screen = screen
		self.viewX, self.viewY = 0,0
			
		# Load the dlw file.
		f = open(filename, 'rb') # World to open!
		
		# Check it's actually a world.
		if f.read(8) != 'SUPREME!':
			die("This isn't a Supreme world.")
		
		# Get world name and builder
		f.seek(8)
		self.builder = null_terminated_string(f.read(32))
		f.seek(40)
		self.name = null_terminated_string(f.read(32))
		
		#Get number of levels
		f.seek(72)
		self.levelCount = ord(f.read(1))
		print self.levelCount, 'levels'
				
		# Get number of tiles
		location = self.load_tiles(f, 77)

		# Level sections
		location = self.load_levels(f, location)
		
	def load_tiles(self, f, offset):
		"""Loads all tile data - images and flags.
		Returns the new file offset."""
		f.seek(offset)
		temp = f.read(2)
		offset += 2
		self.tileCount = unpack16(temp)
		print self.tileCount, 'tiles'
		
		# Grab the tile data!
		tileimages = list()
		for i in range(self.tileCount):
			tileimage, offset = self.load_tile(f, offset)
			tileimages.append(tileimage)
		
		# Extract each tile image in turn and add it to self.tiles
		self.tiles = list()
		current = offset
		for i in range(self.tileCount):
			# Create single tile and add to tile list
			f.seek(current)
			print i, 'Position:', hex(current)
			properties = f.read(4)
			
			# Tile flags
			flags = unpack16(properties[0:2])
			# Animates to:
			animateTo = unpack16(properties[2:4], True)
			
			self.tiles.append( Tile(self, tileimages[i], flags, animateTo) )
			current = current + 4
		return current
		
	def load_tile(self, f, offset):
		"""Creates a single tile image, and returns it and the new file offset."""
		f.seek(offset)
		rletype = unpackBits(f.read(3))
		offset += 3
		
		imagedata = ''
		
		for row in range(24):
			# For each row:
			if rletype[row]:
				#Use RLE
				i = 0
				while i < 32:
					f.seek(offset)
					count = ord(f.read(1)) # Get pixel count
					f.seek(offset+1)
					colour = f.read(1) # Get colour number
					imagedata += colour * count
					# Adjust counters
					offset += 2
					i += count
			else:
				#No RLE
				f.seek(offset)
				imagedata += f.read(32)
				# Adjust counters
				offset += 32
		
		# Create an image from tiledata
		tileimage = pygame.image.fromstring(imagedata, (32, 24), 'P')
		tileimage.set_palette( palette.get_palette())
		tileimage = tileimage.convert(self.screen)
		
		return tileimage, offset
	
	def load_levels(self, f, offset):
		"""Load all the levels in turn, and return the new offset."""
		self.levels = list()
		
		for i in range(1):#self.levelCount):
			l = Level(self, f, offset)
			self.levels.append(l)
			offset = l.get_offset()
		
		self.currentLevel = 0
		self.load_level(self.currentLevel)
	
	def load_level(self, number):
		"""Loads and renders the level."""
		
	def get_tile_image(self, tileNumber):
		"""Returns the tile image of the given id, or a blank surface."""
		if tileNumber >= 0 and tileNumber < len(self.tiles):
			return self.tiles[tileNumber]
		else:
			print "ERROR: Attempting to access non-existant tile", tileNumber
			return False
	
	def draw(self):
		"""Draw the current level."""
		l = self.levels[self.currentLevel]
		
		for y in range(l.height):
			for x in range(l.width):
				self.screen.blit( l.get_tile(x,y).draw(),
					((x*32) - self.viewX, (y*24) - self.viewY) )
