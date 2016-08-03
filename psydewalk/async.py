from threading import Timer
from datetime import datetime, timedelta
import logging

class Alarm():
	"""docstring for Alarm"""
	def __init__(self, sim, logger='alarm'):
		super(Alarm, self).__init__()
		self.sim = sim
		self.logger = logging.getLogger(logger)

	def setup(self, dt, callback, cbargs=None):
		self.alarmtime = dt
		self.callback = callback
		self.cbargs = cbargs

	def start(self):
		dt = self.alarmtime - self.sim.getDatetime()
		self.logger.debug('Alarm activates in {0}'.format(dt))
		self.alarm = Timer(dt.total_seconds(), self.callback, self.cbargs)
		self.alarm.start()

	def cancel(self):
		self.alarm.cancel()
