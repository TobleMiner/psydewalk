from psydewalk.behavior.behaviors import *
from psydewalk.transport.transports import *

class Transport():
	"""docstring for Transport"""
	def __init__(self, behavior): # Behavior is needed to implement walking to bus stops etc
		super(Transport, self).__init__()
		self.behavior = behavior
