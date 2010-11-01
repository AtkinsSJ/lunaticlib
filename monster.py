class Monster:
	"""Dummy monster class"""
	def __init__(self, data):
		self.x = ord(data[0])
		self.y = ord(data[1])
		self.type = ord(data[2])
		self.item = ord(data[3])
		print "Adding monster id", self.type, "carrying", self.item, \
				"to", self.x, self.y
