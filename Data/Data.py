# Data.py - Defines the ways data works in Swail

# Anything that exists in Swail is a DataValue
class DataValue:
	def __init__(self, type, name):
		self.type = type;
		self.name = name;
	
	def Access(self, name):
		try:
			if name.name.value == "name":
				return self.name;
			return getattr(self, name.name.value);
		except KeyError:
			raise Exception(str(self.name) + " doesn't have member " + str(name));

	def Set(self, name, value):
		raise Exception(str(self.name) + " doesn't have member " + str(name));

	def Construct(self, env):
		raise Exception("Cannot construct " + str(self.name));
	
	def Evaluate(self, env):
		raise Exception("Cannot evaluate " + str(self.name));
	
	def __str__(self):
		return "<" + str(self.type) + "> " + str(self.name);
	
	def __eq__(self, other):
		return self is other;
