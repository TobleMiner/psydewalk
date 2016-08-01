
class Behavior():
	"""docstring for Behavior"""
	def __init__(self):
		pass

class Work(Behavior): # TODO Build sequencing for sub-behaviors (drive to work, work, lunch break, work, drive home/somewhere else). Allow mode behaviors to add a hook onto behaviors/groups so they can activate based on those. Maybe also account for national holidays?
	"""docstring for Work"""
	def __init__(self, arg):
		super(Work, self).__init__()
		self.arg = arg

class Vacation(Behavior): # TODO Probably probability based replacement for Work, maybe grouping with probaility based behavior selection
	"""docstring for Vacation"""
	def __init__(self, arg):
		super(Vacation, self).__init__()
		self.arg = arg

class Sleep(Behavior):
	"""docstring for Sleep"""
	def __init__(self, arg):
		super(Sleep, self).__init__()
		self.arg = arg

class Weekend(Behavior):
	"""docstring for Weekend"""
	def __init__(self, arg):
		super(Weekend, self).__init__()
		self.arg = arg
