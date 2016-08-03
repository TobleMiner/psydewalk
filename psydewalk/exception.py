class MethodNotImplementedException(Exception):
	"""docstring for MethodNotImplementedException"""
	def __init__(self):
		super(MethodNotImplementedException, self).__init__('Method not implemented')
		self.arg = arg
