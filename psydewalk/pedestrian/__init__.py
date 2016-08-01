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
		tasks = [
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.355371, 10.131730))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.355249, 10.130726))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.354821, 10.130914))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.353708, 10.131633))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.353442, 10.131874))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.353076, 10.132072))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.352687, 10.132195))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.352406, 10.132247))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.351720, 10.132277))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.350044, 10.132256))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.349564, 10.132307))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.349135, 10.132526))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.348500, 10.132764))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.347040, 10.133016))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.346967, 10.133073))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.346335, 10.133200))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.344824, 10.133198))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.344468, 10.133225))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.344332, 10.133178))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.343625, 10.133296))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.343577, 10.133304))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.342476, 10.133434))),
			asyncio.ensure_future(self.waypoints.put(Coordinate(54.342426, 10.133439)))]
		self.loop.run_until_complete(asyncio.wait(tasks))

	def run(self, interval=50):
		self.logger.info('Starting @{0}'.format(self.loc))
		while True:
			if self.waypoints.empty():
				break
			waypoint = self.loop.run_until_complete(self.waypoints.get())
			self.logger.info('Moving to {0}'.format(waypoint))
			self.moveTo(waypoint, interval)
			self.logger.info('Reached {0}'.format(waypoint))
