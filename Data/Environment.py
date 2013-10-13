# Environment.py - Handles names and such

import Data.Data;
import Data.Lang;
import Data.Type;
import Data.Value;

environmentType = Data.Type.Type("Environment");

# somewhere between a scope and a namespace
class Environment(Data.Data.DataValue):
	def __init__(self, parent, name):
		Data.Data.DataValue.__init__(self, environmentType, name);
		self.vars = {};
		self.parent = parent;
		self.name = name;
		if self.parent != None:
			self.parent.SetVariable(str(self.name), self);
	
	def Evaluate(self):
		return self;

	def Access(self, name):
		if name.type == Data.Value.variableType:
			return self.GetVariable(name.name.value);
		else:
			Data.Data.DataValue.Access(self, name);

	def Set(self, name, value):
		if name.type == Data.Value.variableType:
			self.SetVariable(name.name.value, value);
		else:
			Data.Data.DataValue.Set(self, name, value);

	def GetVariable(self, name):
		if name in self.vars:
			return self.vars[name];
		
		if self.parent == None:
			raise Exception("Unset variable '{}'".format(name));
		
		return self.parent.GetVariable(name);
	
	def HasVariable(self, name):
		if self.parent == None:
			return name in self.vars;
		else:
			return self.parent.HasVariable(name);
	
	def SetVariable(self, name, value, forceHere = False):
		if name in self.vars:
			value.name = name;
			self.vars[name] = value;
		else:
			if forceHere or self.parent == None or not self.parent.HasVariable(name):
				value.name = name;
				self.vars[name] = value;
			else:
				self.parent.SetVariable(name, value);