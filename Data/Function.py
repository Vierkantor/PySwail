# Defines functions in Swail

import Data.Data;
import Data.Type;
import Data.Environment;

functionType = Data.Type.Type("Function");

class Function(Data.Data.DataValue):
	def __init__(self, name, params, optionalParams):
		Data.Data.DataValue.__init__(self, functionType, name);
		self._set("params", params);
		self._set("optionalParams", optionalParams);
	
	def Call(self, callingEnv, args):
		if len(args) < len(self._get("params")):
			return PartialFunction(self, args, self._get("params"), self._get("optionalParams"));
		if len(args) > len(self._get("params")) + len(self._get("optionalParams")):
			raise Exception("Too many arguments for {}, expected {} - {}, received {}.".format(
				str(self),
				len(self._get("params")),
				len(self._get("params")) + len(self._get("optionalParams")),
				len(args),
			));
		
		return self.Exec(callingEnv, args);
		
	def Exec(self, callingEnv, args):
		raise Exception("Cannot call " + str(self));
	
	def __str__(self):
		return "function " + str(self._get("name")) +  "(" + ", ".join(map(str, self._get("params"))) + ")";

class PartialFunction(Function):
	def __init__(self, function, stored, params, optionalParams):
		Function.__init__(self, "{}({})".format(function._get("name"), ", ".join(map(str, stored))), params[len(stored):], optionalParams);
		self._set("stored", stored);
		self._set("function", function);
	
	def Exec(self, callingEnv, args):
		return self._get("function").Call(callingEnv, self._get("stored") + args);

class PredefinedFunction(Function):
	def __init__(self, name, params, optionalParams, function):
		Function.__init__(self, name, params, optionalParams);
		self.function = function;
	
	def Exec(self, callingEnv, args):
		return self.function(callingEnv, args);

class SwailFunction(Function):
	def __init__(self, name, parentEnv, params, optionalParams, block):
		Function.__init__(self, name, params, optionalParams);
		
		self._set("parentEnv", parentEnv);
		self._set("block", block);
	
	def Exec(self, callingEnv, args):
		env = Data.Environment.Environment(self._get("parentEnv"), "<function>");
		i = 0;
		for param in self._get("params") + self._get("optionalParams"):
			try:
				env.SetVariable(param, args[i], True);
				i = i + 1;
			except IndexError:
				break;
		
		result = self._get("block").Evaluate(env);

		return result;
