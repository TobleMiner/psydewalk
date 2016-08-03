class NotImplementedException(Exception):
	"""docstring for NotImplementedException"""
	def __init__(self):
		super(NotImplementedException, self).__init__('Method not implemented')
		self.arg = arg
