#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
from pygame.locals import *
import string

from world import World
from jsp import JSP

#Main class
class Main:
	width = 640
	height = 480
	viewSpeed = 2
	
	def __init__(self):
		# initialize the pygame module
		pygame.init()
		pygame.key.set_repeat(1, 30)
		# load and set the logo
		icon = pygame.image.load("images/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Can you tell what it is yet?")
		
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
		
		self.clock = pygame.time.Clock()
		
		self.jsp = JSP('images/items.jsp', self.screen)
		
		#self.world = World('forest.dlw', self.screen)
		#
		#title = self.world.name + ' by ' + self.world.builder
		#pygame.display.set_caption(title)
		
	def mainLoop(self):
		# define a variable to control the main loop
		self.running = True
		
		# main loop
		while self.running:
			#self.clock.tick(60)
			# event handling, gets all event from the eventqueue
			for event in pygame.event.get():
				# only do something if the event is of type QUIT
				if event.type == pygame.QUIT:
					# change the value to False, to exit the main loop
					self.running = False
				elif event.type == KEYUP:
					if event.key == K_ESCAPE:
						self.running = False
				elif event.type == KEYDOWN:
					if event.key == K_LEFT:
						self.world.viewX -= self.viewSpeed
					elif event.key == K_RIGHT:
						self.world.viewX += self.viewSpeed
					elif event.key == K_UP:
						self.world.viewY -= self.viewSpeed
					elif event.key == K_DOWN:
						self.world.viewY += self.viewSpeed
				elif event.type == pygame.VIDEORESIZE:
					info = pygame.display.Info()
					self.width, self.height = event.size
					pygame.display.set_mode(event.size, pygame.RESIZABLE)
					print "Window resized to", self.width, 'x', self.height
				#	elif event.key == K_SPACE:
				#		pass #self.running = self.level.win()
				#	elif ((event.key == K_RIGHT) or (event.key == K_LEFT)
				#	or (event.key == K_UP) or (event.key == K_DOWN)):
				#		self.level.player.sprite.move(event.key)
			#self.level.update()
			# Drawing
			for i in range(self.jsp.imageCount):
				self.jsp.draw_image(i, self.screen, (32, 32+(64*i)) )
#			self.world.draw()
			#self.screen.blit(self.tileimage, (0,0))
			#self.screen.blit( , (0,0) )
			pygame.display.flip()
	
	
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	Game = Main()
	Game.mainLoop()
