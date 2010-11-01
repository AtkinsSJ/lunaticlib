

class Special:
	"""Dummy special class"""
	INFINITE_USES = -1
	
	def __init__(self, f, offset):
		# Basics
		f.seek(offset)
		data = f.read(4)
		offset += 4
		
		self.x = ord(data[0]) # x
		self.y = ord(data[1]) # y
		self.uses = ord(data[2]) # uses: 0 = infinite
		if self.uses == 0:
			self.uses = Special.INFINITE_USES
		# Number of triggers and effects
		triggerCount = ord(data[3]) & 0b00000111
		effectCount = (ord(data[3]) & 0b11111000) >> 3
		
		print "Creating special at", self.x, self.y, "with", triggerCount, \
			"triggers and", effectCount, "effects. Uses:", self.uses
			
		print "Skipping trigger/effect data for now. Maybe later!"
		offset += (12*triggerCount) + ((12+32)*effectCount)
		
		self.offset = offset
		
	def get_offset(self):
		return self.offset
