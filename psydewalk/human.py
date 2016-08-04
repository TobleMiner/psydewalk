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
		self.loc = loc
		self.setMode(Pedestrian, loc)
		self.controller = BehaviorManager(self)

	def getSimulation(self):
		return self.sim

	def getLocation(self):
		if self.mode:
			return self.mode.getLocation()
		return self.loc

	def getSpeed(self):
		if self.mode:
			return self.mode.getSpeed()
		return -1

	def navigateTo(self, coord):
		self.logger.info('Navigating from {1} to {0}'.format(coord, self.getLocation()))
		self.mode.navigateTo(coord)
		self.mode.run()

	def setMode(self, mode, loc):
		self.logger.info('Setting mode: ' + mode.__name__)
		self.mode = mode(loc)

	def changeMode(self, mode):
		loc = self.mode.getLocation()
		self.setMode(mode, loc)

	def getMode(self):
		return self.mode

	def start(self):
		self.controller.start()
