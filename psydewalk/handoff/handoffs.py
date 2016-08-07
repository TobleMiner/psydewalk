import logging

class Handoff():
	"""docstring for Handoff"""
	DURING = []

	def __init__(self, logger='handoff'):
		super(Handoff, self).__init__()
		self.logger = logging.getLogger(logger)

	def interrupt(self):
		"""Temporary interruption, execution might continue. Don't return from run"""
		self.logger.debug('{0} interrupt'.format(self))

	def notify(self):
		"""Continue execution. Only called after interrupt was called. Don't assume anything about simulation state, recheck everything"""
		self.logger.debug('{0} continue'.format(self))

	def run(self):
		"""Main function. Returning from this function terminates the handoff"""
		self.logger.debug('{0} run'.format(self))

	def terminate(self):
		"""Termination. Return from run as soon as possible"""
		self.logger.debug('{0} terminate'.format(self))

from psydewalk.handoff.park import *
