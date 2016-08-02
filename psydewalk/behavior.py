from psydewalk.pedestrian import Pedestrian
from psydewalk.driver import Driver

from time import sleep
from datetime import time, timedelta, datetime
import random
import logging

class BehaviorManager():
	def __init__(self, human, logger='Behavior'):
		self.logger = logging.getLogger(logger)
		self.human = human
		self.behaviors = []
		self.logger.info('Collecting behaviors')
		self.collectBehaviors(Behavior)
		self.after = {}
		self.logger.info('Building dependency graph')
		self.buildDependencyGraph(Behavior)
		self.groups = {}
		self.logger.info('Building group graph')
		self.buildGroupGraph(Behavior)
		self.logger.info('Data assembled')
		self.logger.debug(repr(self))

	def collectBehaviors(self, cls):
		if (isinstance(cls.AFTER, list) and len(cls.AFTER) > 0) or (not isinstance(cls.AFTER, list) and cls.AFTER):
			self.logger.debug(cls.__name__)
			self.behaviors.append(cls)
		for child in cls.__subclasses__():
			self.collectBehaviors(child)

	def buildDependencyGraph(self, cls):
		for cls_ in cls.AFTER if isinstance(cls.AFTER, list) else [cls.AFTER]:
			if not cls_ in self.after:
				self.after[cls_] = []
			self.after[cls_].append(cls)
			self.logger.debug('{0} -> {1}'.format(cls_.__name__, cls.__name__))
		for child in cls.__subclasses__():
			self.buildDependencyGraph(child)

	def buildGroupGraph(self, cls):
		if cls.GROUP:
			key = cls.GROUP[0]
			self.logger.debug('{0} in {1}'.format(cls.__name__, key))
			if not key in self.groups:
				self.groups[key] = []
			self.groups[key].append(cls)
		for child in cls.__subclasses__():
			self.buildGroupGraph(child)

	def getRandomBehavior(self):
		return random.choice(self.behaviors)

	def __repr__(self):
		string = "\nDependencies:\n"
		for behavior in self.after:
			string += "\t{0}:\n".format(behavior.__name__)
			for ancestor in self.after[behavior]:
				string += "\t\t{0}\n".format(ancestor.__name__)
		string += "Groups\n"
		for group in self.groups:
			string += "\t{0}:\n".format(group)
			for member in self.groups[group]:
				string += "\t\t{0}\n".format(member.__name__)
		return string

	def getNextBehavior(self, behavior): #TODO?MID My eyes are bleeding. Redesign function
		ancestors = []
		now = self.human.getSimulation().getDatetime()
		date = now.date()
		dow = date.weekday()
		time = now.time()
		groups = {} # Collect group information to calculate likelihood
		for ancestor in self.after[behavior]:
			if not dow in ancestor.DOW: # TODO?HIGH: Not going to work. Must do something to wrap around @ midnight
				continue
			begin, end = ancestor.getTimeframe(ancestor, dow)
			eventdate = now
			if time > begin:
				eventdate += timedelta(days=1)
			begin = datetime.combine(eventdate.date(), begin)
			end = datetime.combine(eventdate.date(), end)
			if not ancestor.GROUP:
				ancestors.append((ancestor, begin + (end - begin) * random.random())) # TODO?MID: Don't ignore which behavior would be next
				continue
			key = ancestor.GROUP[0]
			if not key in groups:
				groups[key] = []
				ancestors.append(groups[key])
			groups[key].append(ancestor)
		ancestor = random.choice(ancestors) # Everything has the same likelihood.
		if isinstance(ancestor, list): # We have a group
			probabilitysum = 0
			for behavior in ancestor:
				probabilitysum += behavior.GROUP[1]
			targetval = random.random() * probabilitysum
			for behavior in ancestor:
				targetval -= behavior.GROUP[1]
				if targetval > 0:
					continue
				begin, end = behavior.getTimeframe(behavior, dow)
				eventdate = now
				if time > begin:
					eventdate += timedelta(days=1)
				begin = datetime.combine(eventdate.date(), begin)
				end = datetime.combine(eventdate.date(), end)
				self.logger.debug('NEXT: {0}'.format(behavior))
				return behavior, begin + (end - begin) * random.random()
		self.logger.debug('NEXT: {0}'.format(ancestor[0]))
		return ancestor[0], ancestor[1]

	def getHuman(self):
		return self.human;

	def start(self): # TODO?MID Restore saved state etc
		self.applyBehavior(self.getRandomBehavior())

	def setBehavior(self, behavior):
		self.logger.info('Setting behavior: ' + behavior.__name__)
		self.human.changeMode(behavior.MODE)

	def applyBehavior(self, behavior):
		self.logger.info('Applying behavior: ' + behavior.__name__)
		next = self.getNextBehavior(behavior)[0]
		self.behavior = behavior(self, next)
		#self.human.changeMode(behavior.MODE)
		self.behavior.run()

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

	def __init__(self, mngr, next):
		self.mngr = mngr
		self.next = next
		self.subIndex = 0
		self.parent = None

	def setParent(self, parent):
		self.parent = parent

	def subNext(self):
		if self.subIndex >= len(self.ORDER):
			if self.parent:
				self.parent.subNext()
			else:
				self.mngr.setBehavior(self.next)
				self.mngr.applyBehavior(self.next)
			return
		sub = self.ORDER[self.subIndex]
		self.mngr.setBehavior(sub)
		self.subIndex += 1
		next = self.next
		if self.subIndex < len(self.ORDER):
			next = self.ORDER[self.subIndex]
		elif self.parent:
			next = self.parent.next
		sub = sub(self.mngr, next)
		sub.setParent(self)
		sub.run()

	def run(self):
		self.subNext()

	def done(self):
		self.subNext()

class LocatedBehavior(Behavior):
	"""docstring for LocatedBehavior"""
	def __init__(self, mngr, next):
		super().__init__(mngr, next)

	def getLocation(self):
		raise Exception('Not implemented')

class MoveTo(Behavior):
	"""docstring for moveTo"""
	def __init__(self, mngr, next): # Determine where to drive from location of next behavior
		super().__init__(mngr, next)

	def run(self):
		self.mngr.getHuman().navigateTo(self.next.getLocation(self.mngr.getHuman()))
		self.done()

class DriveTo(MoveTo):
	"""docstring for DriveTo"""
	MODE = Driver
	def __init__(self, mngr, next): # Determine where to drive from location of next behavior
		super().__init__(mngr, next)

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


class Work(Behavior): # TODO Build sequencing for sub-behaviors (drive to work, work, lunch break, work, drive home/somewhere else). Allow mode behaviors to add a hook onto behaviors/groups so they can activate based on those. Maybe also account for national holidays?
	"""docstring for Work"""
	DOW = range(0, 4)
	ACTIVATE = (time(6,30), time(7,20)) # A single tuple indicates that this is the same for all days in a week. If it is an array of tupels each single tuple is used for the corresponding day of week
	GROUP = ('work', 0.95)
	MODE = Pedestrian

	def _init_deps():
		Work.AFTER = Sleep
		Work.ORDER = [DriveTo, Work.DoWork, Break, Work.DoWork, DriveTo]

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


class Vacation(Behavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
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
