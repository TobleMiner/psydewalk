from psydewalk import Simulation
from psydewalk.geo import Coordinate
from psydewalk.pedestrian import Pedestrian
from psydewalk.behavior import BehaviorManager

import logging

class Human():
	"""A human"""
	def __init__(self, sim, loc=Coordinate(), logger='human'):
		self.logger = logging.getLogger(logger)
		self.sim = sim
		self.setMode(Pedestrian, loc)
		self.controller = BehaviorManager(self)
		self.setBehavior(self.controller.getRandomBehavior())

	def getSimulation(self):
		return self.sim

	def setBehavior(self, behavior):
		self.logger.info('Setting behavior: ' + behavior.__name__)
		self.changeMode(behavior.MODE)
		self.behavior = behavior

	def setMode(self, mode, loc):
		self.logger.info('Setting mode: ' + mode.__name__)
		self.mode = mode(loc)

	def changeMode(self, mode):
		loc = self.mode.getLocation()
		self.setMode(mode, loc)
