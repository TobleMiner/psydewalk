from ..entity import SmoothMovingEntity
from ..jitter import Jitter
from ..data import DataProvider
from ..geo import Coordinate

import asyncio
from asyncio import Queue
from threading import Thread


class Pedestrian(SmoothMovingEntity, DataProvider, Jitter):
	def __init__(self, loc=Coordinate(), speed=0, logger='pedestrian'):
		DataProvider.__init__(self)
		Jitter.__init__(self)
		SmoothMovingEntity.__init__(self, loc, speed, logger)
		self.loop = asyncio.get_event_loop()
		self.waypoints = Queue()

	def addWaypoint(self, coord):
		self.loop.run_until_complete(self.waypoints.put(coord))

	def run(self, interval=50):
		self.logger.info('Starting @{0}'.format(self.loc))
		while True:
			waypoint = self.loop.run_until_complete(self.waypoints.get())
			self.logger.info('Moving to {0}'.format(waypoint))
			self.moveTo(waypoint, interval)
			self.logger.info('Reached {0}'.format(waypoint))
