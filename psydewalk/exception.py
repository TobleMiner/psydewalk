class MethodNotImplementedException(Exception):
	"""docstring for MethodNotImplementedException"""
	def __init__(self):
		super(MethodNotImplementedException, self).__init__('Method not implemented')

class NoTransportException(Exception):
	"""docstring for NoTransportException"""
	def __init__(self):
		super(NoTransportException, self).__init__('No common supported transport found')

class MissingInfrastructureException(Exception):
	"""docstring for MissingInfrastructureException"""
	def __init__(self, place, transport):
		super(MissingInfrastructureException, self).__init__('{0} claims to support {1} but has no {2}'.format(place, transport, transport.PLACE))
