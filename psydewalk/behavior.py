from psydewalk.pedestrian import Pedestrian

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
		self.logger.info('Data assembeld')
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

	def getNextBehavior(self, behavior): #TODO My eyes are bleeding. Redesign function
		ancestors = []
		now = self.human.getSimulation().getDatetime()
		date = now.date()
		dow = date.weekday()
		time = now.time()
		groups = {} # Collect group information to calculate likeleyhood
		for ancestor in self.after[behavior]:
			if not dow in ancestor.DOW: # TODO?HIGH: Not going to work. Must do something to wrap around @ midnight
				continue
			begin, end = ancestor.getTimeframe(ancestor, dow)
			eventdate = now
			if time > begin:
				eventdate += timedelta(days=1)
				continue
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
		ancestor = random.choice(ancestors) # Everything has the same likeleyhood.
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
				return behavior, begin + (end - begin) * random.random()
		return ancestor[0], ancestor[1]


class Behavior():
	"""docstring for Behavior"""
	AFTER = []
	GROUP = None
	MODE = Pedestrian

	def getTimeframe(cls, dow):
		if isinstance(cls.ACTIVATE, list):
			interval = cls.ACTIVATE[dow]
			return interval[0], interval[1]
		return cls.ACTIVATE[0], cls.ACTIVATE[1]

	def __init__(self, prev, next):
		self.prev = prev
		self.next = next

	def _init_deps():
		pass

class DriveTo(Behavior):
	"""docstring for DriveTo"""
	def __init__(self, prev, next): # Determine where to drive form prev vs next behavior
		super(DriveTo, self).__init__(self, prev, next)


class Break(Behavior):
	"""docstring for Break""" # Generic break
	def __init__(self, arg):
		super(Break, self).__init__()
		self.arg = arg

class Work(Behavior): # TODO Build sequencing for sub-behaviors (drive to work, work, lunch break, work, drive home/somewhere else). Allow mode behaviors to add a hook onto behaviors/groups so they can activate based on those. Maybe also account for national holidays?
	"""docstring for Work"""
	DOW = range(0, 4)
	ACTIVATE = (time(6,30), time(7,20)) # A single tuple indicates that this is the same for all days in a week. If it is an array of tupels each single tuple is used for the corresponding day of week
	GROUP = ('work', 0.95)
	MODE = Pedestrian

	def _init_deps():
		Work.AFTER = Sleep
		Work.ORDER = [DriveTo, Work.DoWork, Break, Work.DoWork, DriveTo]

	def __init__(self, arg):
		super(Work, self).__init__()
		self.arg = arg

	class DoWork(Behavior):
		"""docstring for DoWork"""
		def __init__(self, arg):
			super(DoWork, self).__init__()
			self.arg = arg

class Vacation(Behavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
	"""docstring for Vacation"""
	DOW = range(0, 4)
	ACTIVATE = (time(8), time(11, 30))
	GROUP = ('work', 0.05)

	def _init_deps():
		Vacation.AFTER = Sleep

	def __init__(self, arg):
		super(Vacation, self).__init__()
		self.arg = arg

class Sleep(Behavior):
	"""docstring for Sleep"""
	DOW = range(0, 6)
	ACTIVATE = (time(22), time(23))

	def _init_deps():
		Sleep.AFTER = [Work, Weekend, Vacation]

	def __init__(self, arg):
		super(Sleep, self).__init__()
		self.arg = arg

class Weekend(Behavior):
	"""docstring for Weekend"""
	DOW = range(5, 6)
	ACTIVATE = (time(9), time(11, 00))

	def _init_deps():
		Weekend.AFTER = Sleep

	def __init__(self, arg):
		super(Weekend, self).__init__()
		self.arg = arg

def init_deps(cls):
	cls._init_deps()
	for cls_ in cls.__subclasses__():
		init_deps(cls_)

init_deps(Behavior)
