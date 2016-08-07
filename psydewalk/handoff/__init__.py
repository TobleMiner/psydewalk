from psydewalk.handoff.handoffs import *

import logging

class HandoffManager():
	"""docstring for HandoffManager"""
	def __init__(self, mngr, logger='handoff'):
		super(HandoffManager, self).__init__()
		self.behaviorManager = mngr
		self.logger = logging.getLogger(logger)
		self.handoffs = []
		self.logger.info('Collecting handoffs')
		self.collectHandoffs(Handoff)
		self.activations = {}
		self.logger.info('Building activation graph')
		self.buildActivationGraph(Handoff)

	def collectHandoffs(self, cls):
		self.logger.debug(cls)
		self.handoffs.append(cls)
		for child in cls.__subclasses__():
			self.collectHandoffs(child)

	def buildActivationGraph(self, cls):
		for activation in cls.DURING if isinstance(cls.DURING, list) else [cls.DURING]:
			activation = self.behaviorManager.getBehavior(activation)
			self.logger.debug('{0} -> {1}'.format(activation, cls))
			if not activation in self.activations:
				self.activations[activation] = []
			self.activations[activation].append(cls)
		for child in cls.__subclasses__():
			self.buildActivationGraph(child)
