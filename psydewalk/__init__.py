from datetime import datetime

__all__ = ['pedestrian', 'tracking']

class Simulation():
	"""docstring for Simulation"""
	def __init__(self):
		super(Simulation, self).__init__()

	def getDatetime(self):
		return datetime.now()
