# Data.py - Defines the ways data works in Swail

# Anything that exists in Swail is a DataValue
class DataValue:
	def __init__(self, type, name):
		self.attrs = {"name": name, "type": type};
	
	def Access(self, name):
		raise Exception(str(self.attrs["name"]) + " doesn't have member " + str(name));
	
	def Insert(self, name, value):
		raise Exception(str(self.attrs["name"]) + " doesn't have member " + str(name));
	
	def _get(self, key):
		return self.attrs[key];
	
	def Get(self, name):
		try:
			return self._get(name._value);
		except (AttributeError, KeyError):
			return self.Access(name);
	
	def _set(self, key, value):
		self.attrs[key] = value;
		return value;
	
	def Set(self, name, value):
		try:
			if name._value in self.attrs:
				return self._set(name._value, value);
		except (AttributeError, KeyError):
			pass;
		
		return self.Insert(name, value);
	
	def Construct(self, env):
		raise Exception("Cannot construct " + str(self.attrs["name"]));
	
	def Evaluate(self, env):
		raise Exception("Cannot evaluate " + str(self.attrs["name"]));
	
	def __str__(self):
		return "<" + str(self.attrs["type"]) + "> " + str(self.attrs["name"]);
	
	def __repr__(self):
		return "<" + str(self.attrs["type"]) + "> " + str(self.attrs["name"]);
