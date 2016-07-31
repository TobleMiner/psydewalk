from ..entity import SmoothMovingEntity
from ..jitter import Jitter
from ..data import DataProvider

from asyncio import Queue
from threading import Thread

class Pedestrian(SmoothMovingEntity, DataProvider, Jitter):
	def __init__(self):
		DataProvider.__init__(self)
		Jitter.__init__(self)
		SmoothMovingEntity.__init__(self)
		self.waypoints = Queue()

	def run(self, interval=100):
		while True:
			waypoint = self.waypoints.get()
			self.moveTo(waypoint, interval)
			
