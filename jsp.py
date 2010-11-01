# JSP loading class

import pygame
from pygame.locals import *

from functions import *
import palette

class JSP:
	"""Loads a .jsp file, and makes the images available."""
	def __init__(self, filename, screen):
		self.screen = screen
		f = open(filename, 'rb') #Open the file
		
		# Image count
		self.imageCount = unpack16(f.read(2))
		
		# Meta
		self.images = list()
		for i in range(self.imageCount):
			bytes = f.read(16)
			w = unpack16(bytes[0:2])
			h = unpack16(bytes[2:4])
			x = -sunpack16(bytes[4:6])
			y = -sunpack16(bytes[6:8])
			size = unpack16(bytes[8:10])
			mystery = bytes[10:]
			self.images.append( JSPImage(w,h,x,y, size) )
		
		# Image data
		for img in self.images:
			img.load_image_data( f.read( img.size ), self.screen )
	
	def get_image(self, id):
		"""Returns the specified image, or False if not found."""
		if (id >= 0) and (id < len(self.images)):
			return self.images[id].image
		else:
			print "ERROR: Trying to access invalid image id:", id
			return False
	
	def draw_image(self, id, surface, position):
		"""Draws the given image onto the surface at the given position,
		taking into account the image's offset."""
		
		if (id >= 0) and (id < len(self.images)):
			img = self.images[id]
		else:
			print "ERROR: Trying to access invalid image id:", id
			return False
			
		realPosition = (position[0] + img.offsetX, position[1] + img.offsetY)
		surface.blit(img.image, realPosition)

class JSPImage:
	"""Holds a single image from a JSP file."""
	def __init__(self, w, h, x, y, size):
		self.width = w
		self.height = h
		self.offsetX = x
		self.offsetY = y
		self.size = size # Size only used by JSP class, but still needs to be held here.
		print "Creating image, size", w, "x", h, "offset", x, ",", y
		
	def load_image_data(self, data, screen):
		"""Give this image some data to gerenate from."""
		
		# Unencode image data
		imagedata = ''
		pos = 0
		while pos < len(data):
			val = ord(data[pos])
			if val > 128:
				imagedata += chr(0)*(val-128)
				pos += 1
			else:
				pos += 1
				for i in range(val):
					imagedata += data[pos+i]
				pos += val
		print len(imagedata), `self.width*self.height`
		
		# Create an image from tiledata
		self.image = pygame.image.fromstring(imagedata, (self.width, self.height), 'P')
		self.image.set_palette( palette.get_palette())
		self.image = self.image.convert(screen)
		self.image.set_colorkey((0,0,0))
		
