class Car(Transport): # TODO?LOW Unserialize transports from human readable config file
	"""docstring for Car"""
	def __init__(self):
		super(Car, self).__init__() # TODO?HIGH Implement behaviors

class Bus(Transport):
	"""docstring for Bus"""
	def __init__(self):
		super(Bus, self).__init__()

class Foot(Transport):
	"""docstring for Foot"""
	def __init__(self, arg):
		super(Foot, self).__init__()

class Bike(Transport):
	"""docstring for Bike"""
	def __init__(self, arg):
		super(Bike, self).__init__()
