# Type.py - Defines the type system in Swail

import Data.Data;

typeType = None;

class Type(Data.Data.DataValue):
	def __init__(self, name):
		Data.Data.DataValue.__init__(self, typeType, name);
		self.subtypes = [];
	
	def AddSubtype(self, type):
		self.subtypes.append(type);
	
	def IsSubtype(self, other):
		if self == other:
			return True;
		else:
			for type in self.subtypes:
				if type.IsSubtype(other):
					return True;
			return False;
	
	def __str__(self):
		return str(self._get("name"));

typeType = Type("Type");
typeType.type = typeType;
noType = Type("Nil");
