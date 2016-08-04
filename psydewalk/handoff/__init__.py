import logging

class HandoffManager():
	"""docstring for HandoffManager"""
	def __init__(self, mngr, logger='handoff'):
		super(HandoffManager, self).__init__()
		self.behaviorManager = mngr
		self.logger = logging.getLogger(logger)
		handoffs = []
		self.logger.info('Collecting handoffs')
		self.collectHandoffs()

	def collectHandoffs(self, cls=Handoff):
		self.logger.debug(cls)
		self.handoffs.append(cls)
		for child in cls.__subclasses__():
			self.collectHandoffs(child)


class Handoff():
	"""docstring for Handoff"""
	def __init__(self):
		super(Handoff, self).__init__()

	def interrupt(self):
		"""Temporary interruption, execution might continue. Don't return from run"""
		pass

	def notify(self):
		"""Continue execution. Only called after interrupt was called. Don't assume anything about simulation state, recheck everything"""
		pass

	def run(self):
		"""Main function. Returning from this function terminates the handoff"""
		pass

	def terminate(self):
		"""Termination. Return from run as soon as possible"""
		pass
