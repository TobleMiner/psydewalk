from psydewalk.behavior.behaviors import *

import random

class Transport():
	"""docstring for Transport"""
	BEHAVIOR = None

	def getTransport(to, from=None):
		if from:
			pass # TODO?MID Code context sensitive transport selection
		transport = to.getSupportedTransports()
		random.choice(transports)

	def __init__(self, registry):
		super(Transport, self).__init__()
		registry.registerTransport(self)

class TransportRegistry():
	"""docstring for TransportRegistry"""
	def __init__(self):
		self.registry = []

	def registerTransport(self, transport):
		self.registry.append(transport)

	def getTransports(self, type):
		transports = []
		for transport in self.registry:
			if isinstance(transport, type):
				transports.append(transport)
		return transports

	def getTransport(self, type):
		transports = self.getTransports(type)
		if len(transports) > 0:
			return random.choice(transports)
