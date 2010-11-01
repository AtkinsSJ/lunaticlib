
from functions import *
from monster import Monster
from special import Special
from leveltile import LevelTile

class Level:
	"""Stores map data for the current level."""
	
	FLAG_SNOW = 1
	FLAG_RAIN = 2
	FLAG_HUB = 4
	FLAG_SECRET = 8
	FLAG_TORCH = 16
	FLAG_LANTERN = 32
	FLAG_STAR = 64
	FLAG_UNDERWATER = 128
	FLAG_UNDERLAVA = 256
	FLAG_STEALTH = 512
	
	def __init__(self, world, f, offset):
		"""Loads the level from the world file.
		To get the new offset, use get_offset()"""
		self.world = world
		self.offset = offset
		self.f = f
		
		# Start data
		f.seek(self.offset)
		data = f.read(66)
		self.offset += 66
		
		self.width = ord(data[0]) # Width
		self.height = ord(data[1]) # Height
		self.name = null_terminated_string(data[2:34]) # Name
		self.song = null_terminated_string(data[34:66]) # Song
		print self.name, self.width, self.height, self.song
		
		self.load_monsters()
		self.load_specials()
		
		# Metadata
		f.seek(self.offset)
		data = f.read(8)
		self.offset += 8
		
		self.flags = unpack16(data[0:2], True)
		self.brainCount = unpack16(data[2:4])
		self.candleCount = unpack16(data[4:6])
		# Ignoring item drop percentage for now
		print self.brainCount, "brains,", self.candleCount, "candles."
		
		# Finally, the map data!
		self.load_map()

	def get_offset(self):
		return self.offset
	
	def load_monsters(self):
		"""Load the monster data for the level."""
		f, o = self.f, self.offset # Shorthand because I am lazy
		
		# Monster count
		f.seek(o)
		monsterCount = ord(f.read(1))
		o+=1
		
		self.monsters = list()
		for i in range(monsterCount):
			f.seek(o)
			self.monsters.append( Monster(f.read(4)) )
			o += 4
		
		self.offset = o
	
	def load_specials(self):
		"""Load the special data for the level."""
		f,o = self.f, self.offset
		
		# Special count
		f.seek(o)
		specialCount = ord(f.read(1))
		o+=1
		
		print "There are", specialCount, "specials."
		
		self.specials = list()
		for i in range(specialCount):
			f.seek(o)
			s = Special(f, o)
			self.specials.append(s)
			o = s.get_offset()
			
		self.offset = o
		
	def load_map(self):
		"""Load the actual map data."""
		f,o = self.f, self.offset
		
		i = 0
		size = self.width * self.height
		
		tiles = list()
		
		while (i < size):
			f.seek(o)
			rl = ord(f.read(1))
			o += 1
			
			if rl >= 128: # Runlength encoding!
				rl = 256 - rl
				f.seek(o)
				data = f.read(6)
				o += 6
				
				floor = unpack16(data[0:2])
				wall = unpack16(data[2:4])
				item = ord(data[4])
				lighting = ord(data[5])
				print "Creating", rl, "tiles with floor/wall/item/lighting:", \
					floor, wall, item, lighting
					
				floor = self.world.get_tile_image(floor)
				if wall != 0:
					wall = self.world.get_tile_image(wall)
				else:
					wall = False
				
				for j in range(rl):
					tiles.append(LevelTile(floor, wall, item, lighting))
				i += rl
			else: # Load in this many tiles!
				for j in range(rl):
					f.seek(o)
					data = f.read(6)
					o += 6
					
					floor = unpack16(data[0:2])
					wall = unpack16(data[2:4])
					item = ord(data[4])
					lighting = ord(data[5])
					print "Creating 1 tile with floor/wall/item/lighting:", \
						floor, wall, item, lighting
						
					floor = self.world.get_tile_image(floor)
					if wall != 0:
						wall = self.world.get_tile_image(wall)
					else:
						wall = False
					tiles.append(LevelTile(floor, wall, item, lighting))
				i += rl
		print len(tiles), 'tiles, should be', size
		
		# Sort tiles into proper array
		self.map = list()
		for y in range(self.height):
			row = tiles[y*self.width:(y+1)*self.width]
			self.map.append(row)
					
		self.offset = o
		
	def get_tile(self, x, y):
		"""Returns the given tile, or False if location is invalid."""
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			return self.map[y][x]
		else:
			return False
