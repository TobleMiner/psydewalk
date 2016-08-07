from psydewalk.pedestrian import Pedestrian
from psydewalk.driver import Driver
from psydewalk.data import LocationProvider, PlaceProvider
from psydewalk.util.list import intersect
from psydewalk.exception import MethodNotImplementedException, NoTransportException
import psydewalk.place.places as PLACES

from time import sleep
from datetime import time, timedelta, datetime
from collections import deque
from threading import Lock
import random
import logging

class Behavior():
	"""docstring for Behavior"""
	AFTER = []
	GROUP = None
	MODE = Pedestrian
	ORDER = []
	HANDOFF = False

	def getTimeframe(cls, dow):
		if isinstance(cls.ACTIVATE, list):
			interval = cls.ACTIVATE[dow]
			return interval[0], interval[1]
		return cls.ACTIVATE[0], cls.ACTIVATE[1]

	def _init_deps():
		pass

	def __init__(self, mngr, parent=None, deadline=None):
		self.logger = logging.getLogger(type(self).__name__)
		self.mngr = mngr
		self.parent = parent
		self.deadline = deadline
		self.queue = deque()
		self.terminated = False
		self.doTerminate = False
		self.sub = None
		self.subLock = Lock()
		self.init()

	def setDeadline(self, deadline):
		self.deadline = deadline

	def getTimeLeft(self):
		return self.deadline - self.mngr.getHuman().getSimulation().getDatetime()

	def terminate(self):
		if self.terminated:
			return
		self.doTerminate = True
		self.logger.warning('Behavior {0} failed to terminate in time. Terminating'.format(self))
		self.subLock.acquire()
		self.queue.clear()
		if self.sub:
			self.sub.terminate()
		mode = self.mngr.getHuman().getMode()
		if mode:
			self.logger.debug('Got mode {0} Terminated: {1}'.format(mode, mode.terminated))
			self.logger.debug('Terminating mode')
			mode.terminate()
			assert mode.terminated, "Mode didn't terminate"
		self.cleanup()

	def cleanup(self):
		"""Perform cleanup"""
		self.logger.debug('Cleaning up {0}'.format(self))

	def init(self):
		"""Performs pre instantiation initialisation (dynamic sub-behaviors and such)"""
		pass

	def initPrev(self, prev):
		"""Initializes this instance based on the previous behavior"""
		pass

	def initSub(self):
		for sub in self.ORDER if isinstance(self.ORDER, list) else [self.ORDER]:
			self.queue.append(sub(self.mngr, self))

	def preSub(self):
		pass

	def postSub(self):
		pass

	def subNext(self):
		if self.doTerminate:
			return
		if len(self.queue) == 0:
			if self.parent:
				self.parent.subNext()
		else:
			self.subLock.acquire()
			self.sub = self.queue.popleft()
			self.subLock.release()
			self.sub.run()

	def run(self):
		self.mngr.setBehavior(self)
		if self.doTerminate:
			return
		self.preSub()
		self.subNext()
		if self.doTerminate:
			return
		self.mngr.setBehavior(self)
		self.postSub()
		self.terminated = True

class LocatedBehavior(Behavior, LocationProvider):
	"""docstring for LocatedBehavior"""

	def __init__(self, mngr, parent=None, deadline=None):
		super(LocatedBehavior, self).__init__(mngr, parent, deadline)
		self.setLocation()

	def cleanup(self):
		super(LocatedBehavior, self).cleanup()
		sub = TransportBehavior(self.mngr) # Don't set parent. Run detached
		sub.initTransport(None, self)
		sub.run()

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

	def __init__(self, mngr, parent=None, deadline=None):
		super(PlacedBehavior, self).__init__(mngr, parent, deadline)
		self.setPlace()

	def cleanup(self):
		super(PlacedBehavior, self).cleanup()
		sub = TransportBehavior(self.mngr) # Don't set parent. Run detached
		sub.initTransport(None, self)
		sub.run()

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
	def __init__(self, mngr, parent=None, deadline=None, logger='transport'):
		super(TransportBehavior, self).__init__(mngr, parent, deadline)
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
		from psydewalk.transport.transports import Car
		transport = random.choice(transports)
		transports = Car
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

	def preSub(self):
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
	DOW = range(0, 7)
	ACTIVATE = (time(6,30), time(7,20)) # A single tuple indicates that this is the same for all days in a week. If it is an array of tupels each single tuple is used for the corresponding day of week
	GROUP = ('work', 0.95)
	MODE = Pedestrian

	def _init_deps():
		Work.AFTER = Sleep
		Work.ORDER = [Work.DoWork, Work.LunchBreak, Work.DoWork]

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

	class LunchBreak(Break):
		"""docstring for LunchBreak"""
		HANDOFF = True


class Vacation(PlacedBehavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
	"""docstring for Vacation"""
	DOW = range(0, 4)
	ACTIVATE = (time(8), time(11, 30))
	GROUP = ('work', 0.05)
	MODE = Pedestrian
	HANDOFF = True

	def _init_deps():
		Vacation.AFTER = Sleep

	def setPlace(self):
		self.place = self.mngr.getHuman().getSimulation().getPlaceRegistry().getPlace(PLACES.Home)


class Sleep(PlacedBehavior):
	"""docstring for Sleep"""
	DOW = range(0, 7)
	ACTIVATE = (time(22), time(23))
	MODE = Pedestrian

	def _init_deps():
		Sleep.AFTER = [Work, Weekend, Vacation]

	def setPlace(self):
		self.place = self.mngr.getHuman().getSimulation().getPlaceRegistry().getPlace(PLACES.Home)

class Weekend(Behavior):
	"""docstring for Weekend"""
	DOW = range(5, 7)
	ACTIVATE = (time(9), time(11, 00))
	MODE = Pedestrian

	def _init_deps():
		Weekend.AFTER = Sleep


def init_deps(cls):
	cls._init_deps()
	for cls_ in cls.__subclasses__():
		init_deps(cls_)

init_deps(Behavior)
