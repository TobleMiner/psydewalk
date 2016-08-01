import datetime.time as time

class Behavior():
	"""docstring for Behavior"""
	def __init__(self):
		pass

class Work(Behavior): # TODO Build sequencing for sub-behaviors (drive to work, work, lunch break, work, drive home/somewhere else). Allow mode behaviors to add a hook onto behaviors/groups so they can activate based on those. Maybe also account for national holidays?
	"""docstring for Work"""
	DOW = range(0, 4)
	ACTIVATE = (time(6,30), time(7,20)) # A single tuple indicates that this is the same for all days in a week. If it is an array of tupels each single tuple is used for the corresponding day of week
	AFTER = Sleep
	GROUP = ('work', 0.95)
	def __init__(self, arg):
		super(Work, self).__init__()
		self.arg = arg

class Vacation(Behavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
	"""docstring for Vacation"""
	DOW = range(0, 4)
	ACTIVATE = (time(8), time(11, 30))
	AFTER = Sleep
	GROUP = ('work', 0.05)
	def __init__(self, arg):
		super(Vacation, self).__init__()
		self.arg = arg

class Sleep(Behavior):
	"""docstring for Sleep"""
	DOW = range(0, 6)
	ACTIVATE = (time(22), time(23))
	AFTER = [Work, Weekend, Vacation]
	def __init__(self, arg):
		super(Sleep, self).__init__()
		self.arg = arg

class Weekend(Behavior):
	"""docstring for Weekend"""
	DOW = range(5, 6)
	ACTIVATE = (time(9), time(11, 00))
	AFTER = Sleep
	def __init__(self, arg):
		super(Weekend, self).__init__()
		self.arg = arg
