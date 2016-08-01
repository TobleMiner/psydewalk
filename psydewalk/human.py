import psydewalk.geo.Coordinate
from psydewalk.pedestrian import Pedestrian

class Human():
	"""A human"""
	def __init__(self, loc=Coordinate()):
		self.setMode(Pedestrian, loc)
		self.controller = BehaviorController()

	def setMode(self, mode, loc):
		self.mode = mode(loc)

	def changeMode(self, mode):
		loc = self.mode.getLocation()
		self.mode = mode(loc)

class BehaviorController():
	__init__(self, human):
		self.human = human
