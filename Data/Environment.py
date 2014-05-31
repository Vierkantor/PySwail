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
		self._set("vars", Data.Value.Dict({}));
		
		self._set("parent", parent);
		# add a reference to ourselves in our parent
		if self._get("parent") != None:
			self._get("parent").SetVariable(Data.Value.Variable(str(self._get("name"))), self);
	
	def Evaluate(self):
		return self;
	
	def Access(self, name):
		if Data.Value.variableType.IsSubtype(name._get("type")):
			return self.GetVariable(name);
		else:
			Data.Data.DataValue.Access(self, name);
	
	def Insert(self, name, value):
		if Data.Value.variableType.IsSubtype(name._get("type")):
			self.SetVariable(name, value);
		else:
			Data.Data.DataValue.Insert(self, name, value);
	
	def GetVariable(self, name):
		if name in self._get("vars"):
			return self._get("vars").Access(name);
		
		if self._get("parent") == None:
			raise Exception("Unset variable '{}'".format(repr(name)));
		
		return self._get("parent").GetVariable(name);
	
	def HasVariable(self, name):
		if self._get("parent") == None:
			return name._value in self._get("vars");
		else:
			return self._get("parent").HasVariable(name);
	
	def SetVariable(self, name, value, forceHere = False):
		if forceHere or name._value in self._get("vars") or not (self._get("parent") != None and self._get("parent").HasVariable(name)):
			value._set("name", name);
			self._get("vars").Insert(name, value);
		else:
			self._get("parent").SetVariable(name, value);
	
	def __str__(self):
		return "<Environment> " + str(self._get("name")) + ": [" + ", ".join(map(str, self._get("vars")._value)) + "]";
