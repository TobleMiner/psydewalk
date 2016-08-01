import random

# Behaviors triggered by changing behavior of a human 

class Behavior():
	"""Some behavior"""
	def __init__(self):
		self.duration = random.randint(self.DURATION[0], self.DURATION[1])

class Break(Behavior):
	"""A pedestrian taking a break"""
	DURATION = (300, 3600) # TODO Use environmental data to adjust break length and delay between breaks
	DELAY = (1800, 14400)
	def __init__(self):
		super().__init__(self)
