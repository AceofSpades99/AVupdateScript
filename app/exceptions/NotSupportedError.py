class NotSupportedError(Exception):
	def __init__(self, message='Sistema operativo no soportado'):
		self.message = message
		super().__init__(self.message)
