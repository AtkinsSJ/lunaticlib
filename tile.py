class Tile:
	"""A tile type, as defined in the Tiles menu."""
	# Tile Flags
	FLAG_IMPASSABLE = 1
	FLAG_ICY = 2
	FLAG_MUDDY = 4
	FLAG_WATER = 8
	FLAG_LAVA = 16
	FLAG_PUSHABLE = 32
	FLAG_CAN_PUSH_ON = 64
	FLAG_ANIMATES_TO_NEXT = 128
	FLAG_ANIMATES_ON_STEP = 256
	FLAG_ANIMATES_WHEN_HIT = 512
	FLAG_TRANSPARENT_ROOF = 1024
	FLAG_MINECART_PATH = 2048
	FLAG_BUNNY_PATH = 4096
	FLAG_GHOST_PROOF = 8192
	FLAG_ENEMY_PROOF = 16384
	FLAG_BOUNCY = 32768
	
	def __init__(self, world, image, flags=0, animateTo=0):
		self.world = world
		self.image = image
		self.flags = flags
		if self.flags & Tile.FLAG_TRANSPARENT_ROOF:
			self.image.set_colorkey((0,0,0))
		self.animateTo = animateTo
		print 'New tile, flags:', bin(self.flags), 'Animates to:', self.animateTo
		
	def draw(self):
		return self.image
		
	def flag(self, flag):
		return self.flags & flag
