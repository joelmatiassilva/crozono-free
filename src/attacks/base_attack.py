import abc

class BaseAttack(abc.ABC):

	def __init__(self):
		pass

	@abc.abstractmethod
	def run(self):
		pass

	@abc.abstractmethod
	def check(self):
		pass

	@abc.abstractmethod
	def setup(self):
		pass