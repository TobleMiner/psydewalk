from psydewalk.pedestrian import Pedestrian
from psydewalk.driver import Driver
from psydewalk.place.places import *
from psydewalk.data import LocationProvider, PlaceProvider
from psydewalk.util.list import intersect
from psydewalk.exception import MethodNotImplementedException, NoTransportException
import psydewalk.place.places as PLACES

from time import sleep
from datetime import time, timedelta, datetime
import random
import logging

class Behavior():
	"""docstring for Behavior"""
	AFTER = []
	GROUP = None
	MODE = Pedestrian
	ORDER = []

	def getTimeframe(cls, dow):
		if isinstance(cls.ACTIVATE, list):
			interval = cls.ACTIVATE[dow]
			return interval[0], interval[1]
		return cls.ACTIVATE[0], cls.ACTIVATE[1]

	def _init_deps():
		pass

	def __init__(self, mngr, parent=None, timelimit=None):
		self.mngr = mngr
		self.parent = parent
		self.timelimit = timelimit
		self.queue = []
		self.init()

	def init(self):
		"""Performs pre instanziation initialisation (dynamic sub-behaviors and such)"""
		pass

	def initPrev(self, prev):
		"""Initializes this instance based on the previous behavior"""
		pass

	def initSub(self):
		for sub in self.ORDER:
			self.queue.append(sub(self.mngr, self))

	def preSub(self):
		pass

	def postSub(self):
		pass

	def subNext(self):
		if len(self.queue) == 0:
			self.run()
			if self.parent:
				self.parent.subNext()
			else:
				return #self.mngr.runNext(self)
		sub = self.queue.pop(0)
		sub.run()

	def run(self):
		self.mngr.setBehavior(self)
		self.preSub()
		self.subNext()
		self.postSub()

class LocatedBehavior(Behavior, LocationProvider):
	"""docstring for LocatedBehavior"""

	def __init__(self, mngr, parent=None, timelimit=None):
		super(LocatedBehavior, self).__init__(mngr, parent, timelimit)
		self.setLocation()

	def setLocation(self):
		print(self)
		raise MethodNotImplementedException()

	def getLocation(self):
		return self.loc

	def initPrev(self, prev):
		sub = TransportBehavior(self.mngr, self)
		sub.initTransport(prev, self)
		self.queue.append(sub)

class PlacedBehavior(Behavior, PlaceProvider):
	"""docstring for PlacedBehavior"""

	def __init__(self, mngr, parent=None, timelimit=None):
		super(PlacedBehavior, self).__init__(mngr, parent, timelimit)
		self.setPlace()

	def setPlace(self):
		raise MethodNotImplementedException()

	def getPlace(self):
		return self.place

	def initPrev(self, prev):
		sub = TransportBehavior(self.mngr, self)
		sub.initTransport(prev, self)
		self.queue.append(sub)


class TransportBehavior(Behavior):
	"""docstring for TransportBehavior"""
	def __init__(self, mngr, parent=None, timelimit=None, logger='transport'):
		super(TransportBehavior, self).__init__(mngr, parent, timelimit)
		self.logger = logging.getLogger(logger)

	def initTransport(self, frm, to):
		self.logger.debug('Transport: {0} -> {1}'.format(frm, to))
		transports = self.mngr.getHuman().getSimulation().getTransportRegistry().getTransports()
		locfrm = frm
		if isinstance(frm, PlaceProvider):
			place = frm.getPlace()
			transports = place.getSupportedTransports()
			locfrm = place.getLocation()
		elif isinstance(frm, LocationProvider):
			locfrm = frm.getLocation()
		else:
			pass
		locto = to
		if isinstance(to, PlaceProvider):
			place = to.getPlace()
			transports = intersect(transports, place.getSupportedTransports())
			locto = place.getLocation()
		elif isinstance(to, LocationProvider):
			locto = to.getLocation()
		else:
			pass
		if len(transports) == 0:
			raise NoTransportException()
		transport = random.choice(transports)
		self.logger.debug('Choosen transport: {0}'.format(transport))
		behavior = self.mngr.getBehavior(transport.BEHAVIOR)
		if transport.PLACE:
			start = locfrm
			if isinstance(frm, PlaceProvider):
				start = self.getEndpointfromPlace(frm.getPlace(), transport)
				self.queue.append(WalkTo(self.mngr, self, start))
			end = locto
			if isinstance(to, PlaceProvider):
				end = self.getEndpointfromPlace(to.getPlace(), transport)
				self.queue.append(behavior(self.mngr, self, end))
				self.queue.append(WalkTo(self.mngr, self, locto))
			else:
				self.queue.append(behavior(self.mngr, self, end))
		else:
			self.queue.append(behavior(self.mngr, self, locto))

	def getEndpointfromPlace(self, place, transport):
		endpoint = place.getTransportEndpoint(transport)
		if isinstance(endpoint, list):
			return random.choice(endpoint).getLocation()
		return endpoint.getLocation()


class MoveTo(Behavior):
	"""docstring for MoveTo"""

	def __init__(self, mngr, parent, to):
		super().__init__(mngr, parent)
		self.dest = to

	def postSub(self):
		self.mngr.getHuman().navigateTo(self.dest)

class WalkTo(MoveTo):
	"""docstring for moveTo"""
	MODE = Pedestrian

class DriveTo(MoveTo):
	"""docstring for DriveTo"""
	MODE = Driver

class Break(Behavior):
	"""docstring for Break""" # Generic break
	MODE = Pedestrian
	DURATION = (1, 10)

	def init(self):
		self.duration = random.randint(self.DURATION[0], self.DURATION[1])

	def postSub(self):
		sleep(self.duration)

class Work(PlacedBehavior): # TODO Build sequencing for sub-behaviors (drive to work, work, lunch break, work, drive home/somewhere else). Allow mode behaviors to add a hook onto behaviors/groups so they can activate based on those. Maybe also account for national holidays?
	"""docstring for Work"""
	DOW = range(0, 4)
	ACTIVATE = (time(6,30), time(7,20)) # A single tuple indicates that this is the same for all days in a week. If it is an array of tupels each single tuple is used for the corresponding day of week
	GROUP = ('work', 0.95)
	MODE = Pedestrian

	def _init_deps():
		Work.AFTER = Sleep
		Work.ORDER = [Work.DoWork, Break, Work.DoWork]

	def setPlace(self):
		self.place = self.mngr.getHuman().getSimulation().getPlaceRegistry().getPlace(PLACES.Work)

	class DoWork(Behavior):
		"""docstring for DoWork"""
		DURATION = (3, 30)
		MODE = Pedestrian

		def init(self):
			self.duration = random.randint(self.DURATION[0], self.DURATION[1])

		def postSub(self):
			sleep(self.duration)


class Vacation(PlacedBehavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
	"""docstring for Vacation"""
	DOW = range(0, 4)
	ACTIVATE = (time(8), time(11, 30))
	GROUP = ('work', 0.05)
	MODE = Pedestrian

	def _init_deps():
		Vacation.AFTER = Sleep

	def setPlace(self):
		self.place = self.mngr.getHuman().getSimulation().getPlaceRegistry().getPlace(PLACES.Home)


class Sleep(PlacedBehavior):
	"""docstring for Sleep"""
	DOW = range(0, 6)
	ACTIVATE = (time(22), time(23))
	MODE = Pedestrian

	def _init_deps():
		Sleep.AFTER = [Work, Weekend, Vacation]

	def setPlace(self):
		self.place = self.mngr.getHuman().getSimulation().getPlaceRegistry().getPlace(PLACES.Home)

class Weekend(Behavior):
	"""docstring for Weekend"""
	DOW = range(5, 6)
	ACTIVATE = (time(9), time(11, 00))
	MODE = Pedestrian

	def _init_deps():
		Weekend.AFTER = Sleep


def init_deps(cls):
	cls._init_deps()
	for cls_ in cls.__subclasses__():
		init_deps(cls_)

init_deps(Behavior)
