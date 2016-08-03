from psydewalk.pedestrian import Pedestrian
from psydewalk.driver import Driver
from psydewalk.place.places import *
from psydewalk.data import LocationProvider

from time import sleep
from datetime import time, timedelta, datetime
import random

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

	def __init__(self, mngr, parent=None):
		self.mngr = mngr
		self.parent = parent
		self.queue = []
		for sub in self.ORDER:
			self.queue.append(sub(mngr, self))
		self.init()

	def init(self):
		"""Performs pre instanziation initialisation (dynamic sub behaviors and such)"""
		pass

	def subNext(self):
		if len(self.queue) == 0:
			if self.parent:
				self.parent.subNext()
			else:
				self.mngr.runNext(self)
		sub = self.queue.pop(0)
		sub.run()

	def run(self):
		self.subNext()

	def done(self):
		self.subNext()

class LocatedBehavior(Behavior, LocationProvider):
	"""docstring for LocatedBehavior"""
	PLACE = None

	@classmethod
	def hasPlace(cls):
		return cls.PLACE != None

	def __init__(self, mngr, next):
		super().__init__(mngr, next)

class TransportBehavior(Behavior):
	"""docstring for TransportBehavior"""
	MODE = Pedestrian

	def __init__(self, mngr, next, transport, to, frm=None):
		super(TransportBehavior, self).__init__(mngr, next)
		self.transport = transport
		if not frm:
			frm = mngr.getHuman().getLocation()
		transportfrm = frm
		if isinstance(frm, Place):
			transportfrm = self.getEndpointfromPlace(frm, transport).getLocation()
		transportto = to
		locto = to
		if isinstance(to, Place):
			transportto = self.getEndpointfromPlace(to, transport).getLocation
			locto = to.getLocation()
		self.next = WalkTo(mngr, transport.BEHAVIOR(mngr, WalkTo(mngr, self.next, locto), transportto), transportfrm)
		transport.BEHAVIOR(mngr, transportto)

	def getEndpointfromPlace(self, place, transport):
		endpoint = place.getTransportEndpoint(transport)
		if isinstance(endpoint, list):
			return random.choice(endpoint)
		return endpoint


class MoveTo(Behavior):
	"""docstring for MoveTo"""

	def __init__(self, mngr, next, loc): # Determine where to drive frm location of next behavior
		super().__init__(mngr, next)
		self.loc = loc

	def run(self):
		self.mngr.getHuman().navigateTo(self.loc)
		self.done()

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
	def __init__(self, mngr, next):
		super().__init__(mngr, next)
		self.duration = random.randint(self.DURATION[0], self.DURATION[1])

	def run(self):
		sleep(self.duration)
		self.done()

class Work(LocatedBehavior): # TODO Build sequencing for sub-behaviors (drive to work, work, lunch break, work, drive home/somewhere else). Allow mode behaviors to add a hook onto behaviors/groups so they can activate based on those. Maybe also account for national holidays?
	"""docstring for Work"""
	DOW = range(0, 4)
	ACTIVATE = (time(6,30), time(7,20)) # A single tuple indicates that this is the same for all days in a week. If it is an array of tupels each single tuple is used for the corresponding day of week
	GROUP = ('work', 0.95)
	MODE = Pedestrian
	PLACE = Work()

	def _init_deps():
		Work.AFTER = Sleep
		Work.ORDER = [Work.DoWork, Break, Work.DoWork]

	def __init__(self, mngr, next):
		super().__init__(mngr, next)

	def run(self):
		self.subNext()

	class DoWork(LocatedBehavior):
		"""docstring for DoWork"""
		DURATION = (3, 30)
		MODE = Pedestrian

		def __init__(self, mngr, next):
			super().__init__(mngr, next)
			self.duration = random.randint(self.DURATION[0], self.DURATION[1])

		def getLocation(human):
			return human.attributes['work']['loc'] # TODO?LOW Implement proper extensible attributes

		def run(self):
			sleep(self.duration)
			self.done()


class Vacation(LocatedBehavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
	"""docstring for Vacation"""
	DOW = range(0, 4)
	ACTIVATE = (time(8), time(11, 30))
	GROUP = ('work', 0.05)
	MODE = Pedestrian

	def _init_deps():
		Vacation.AFTER = Sleep

	def __init__(self, mngr, next):
		super().__init__(mngr, next)

class Sleep(LocatedBehavior):
	"""docstring for Sleep"""
	DOW = range(0, 6)
	ACTIVATE = (time(22), time(23))
	MODE = Pedestrian
	PLACE = Home()

	def _init_deps():
		Sleep.AFTER = [Work, Weekend, Vacation]

	def getLocation(human):
		return human.attributes['home']['loc'] # TODO?LOW Implement proper extensible attributes

	def __init__(self, mngr, next):
		super().__init__(mngr, next)

class Weekend(Behavior):
	"""docstring for Weekend"""
	DOW = range(5, 6)
	ACTIVATE = (time(9), time(11, 00))
	MODE = Pedestrian

	def _init_deps():
		Weekend.AFTER = Sleep

	def __init__(self, mngr, next):
		super().__init__(mngr, next)

def init_deps(cls):
	cls._init_deps()
	for cls_ in cls.__subclasses__():
		init_deps(cls_)

init_deps(Behavior)
