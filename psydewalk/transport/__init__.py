import random

class Transport():
	"""docstring for Transport"""
	BEHAVIOR = None

	def __init__(self, registry):
		super(Transport, self).__init__()
		registry.registerTransport(self)

class TransportRegistry():
	"""docstring for TransportRegistry"""
	def __init__(self):
		self.transports = []
		self.collectTransports()
		self.registry = []

	def collectTransports(self, cls=Transport):
		if cls.BEHAVIOR:
			self.transports.append(cls)
		for child in self.transports.__subclasses__:
			self.collectTransports(child)

	def registerTransport(self, transport):
		self.registry.append(transport)

	def getSupportedTransport(self, frm=None, to=None):
		return random.choice(self.getSupportedTransports(to, frm))

	def getSupportedTransports(self, frm=None, to=None):
		if not to and not frm:
			return self.transports
		transportsto = self.transports
		if to:
			transportsto = to.getSupportedTransports()
		transportsfrm = self.transports
		if frm:
			transportsfrm = frm.getSupportedTransports()
		return [list(filter(lambda transport: transport in transportsfrm, transports)) for transports in transportsto]

	def getTransports(self, type=None):
		if not type:
			return self.registry
		transports = []
		for transport in self.registry:
			if isinstance(transport, type):
				transports.append(transport)
		return transports

	def getTransport(self, type):
		transports = self.getTransports(type)
		if len(transports) > 0:
			return random.choice(transports)
