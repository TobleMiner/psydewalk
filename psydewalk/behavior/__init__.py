from datetime import time, timedelta, datetime
import random
import logging

from psydewalk.behavior.behaviors import Behavior

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
		behavior = type(behavior)
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
				self.logger.debug('NEXT: {0}'.format(behavior))
				return behavior, begin + (end - begin) * random.random()
		self.logger.debug('NEXT: {0}'.format(ancestor[0]))
		return ancestor[0], ancestor[1]

	def getHuman(self):
		return self.human;

	def start(self): # TODO?MID Restore saved state etc
		self.runNext(None)

	def runNext(self, prev):
		behavior = self.getNextBehavior(prev)[0]
		self.logger.debug(behavior)
		behavior = behavior(self)
		behavior.initPrev(prev)
		behavior.initSub()
		self.run(behavior)

	def run(self, behavior):
		behavior._run()

	def setBehavior(self, behavior):
		self.logger.info('Setting behavior: ' + type(behavior).__name__)
		self.human.changeMode(behavior.MODE)
