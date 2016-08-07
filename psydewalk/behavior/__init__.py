from datetime import time, timedelta, datetime
from threading import Lock
import random
import logging

from psydewalk.behavior.behaviors import Behavior
from psydewalk.async import Alarm
from psydewalk.handoff import HandoffManager

class BehaviorManager():
	def __init__(self, human, logger='Behavior'):
		self.logger = logging.getLogger(logger)
		self.human = human
		self.behaviors = []
		self.logger.info('Collecting behaviors')
		self.collectBehaviors(Behavior)
		self.behaviorByName = {}
		self.logger.info('Building name -> behavior relationship')
		self.buildNameBehaviorRelation(Behavior)
		self.after = {}
		self.logger.info('Building dependency graph')
		self.buildDependencyGraph(Behavior)
		self.groups = {}
		self.logger.info('Building group graph')
		self.buildGroupGraph(Behavior)
		self.logger.info('Data assembled')
		self.logger.debug(repr(self))
		self.handoff = HandoffManager(self)
		self.behaviorLock = Lock()
		self.next = None
		self.alarm = None

	def collectBehaviors(self, cls):
		if (isinstance(cls.AFTER, list) and len(cls.AFTER) > 0) or (not isinstance(cls.AFTER, list) and cls.AFTER):
			self.logger.debug(cls.__name__)
			self.behaviors.append(cls)
		for child in cls.__subclasses__():
			self.collectBehaviors(child)

	def buildNameBehaviorRelation(self, cls):
		self.behaviorByName[cls.__name__] = cls
		for child in cls.__subclasses__():
			self.buildNameBehaviorRelation(child)

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

	def getBehavior(self, name):
		return self.behaviorByName[name]

	def getRandomBehavior(self):
		from psydewalk.behavior.behaviors import Work
		return Work # return 4 TODO?DEBUG
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
		now = self.human.getSimulation().getDatetime()
		if not behavior:
			return (self.getRandomBehavior(), now)
		ancestors = []
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
				return behavior, begin + (end - begin) * random.random()
		return ancestor[0], ancestor[1]

	def getHuman(self):
		return self.human;

	def start(self): # TODO?MID Restore saved state etc
		self.runNext(None)

	def runNext(self, prev):
		behavior = self.next
		if prev:
			prev.terminate()
		self.behaviorLock.acquire()
		if not behavior:
			behavior = self.getNextBehavior(type(prev) if prev else None)[0]
		self.logger.debug('Starting behavior: {0}'.format(behavior))
		self.next, time = self.getNextBehavior(behavior)
		time = self.human.getSimulation().getDatetime() + timedelta(seconds=20)
		behavior = behavior(self, deadline=time)
		self.alarm = Alarm(self.human.getSimulation())
		self.logger.debug('Deadline for {0} set: {1}'.format(behavior, time))
		self.logger.debug('Next behavior: {0}@{1}'.format(self.next, time))
		self.alarm.setup(time, self.runNext, [behavior])
		self.alarm.start()
		behavior.initPrev(prev)
		behavior.initSub()
		self.run(behavior)
		self.behaviorLock.release()

	def run(self, behavior):
		behavior.run()

	def setBehavior(self, behavior):
		self.logger.info('Setting behavior: ' + type(behavior).__name__)
		self.human.changeMode(behavior.MODE)
