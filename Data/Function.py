# Defines functions in Swail

import Data.Data;
import Data.Type;
import Data.Environment;

functionType = Data.Type.Type("Function");

class Function(Data.Data.DataValue):
	def __init__(self, name, params):
		Data.Data.DataValue.__init__(self, functionType, name);
		self.params = params;
	
	def Call(self, callingEnv, args):
		if len(args) < len(self.params):
			return PartialFunction(self.params, args, self);
		if len(args) > len(self.params):
			raise Exception("Too many arguments for " + str(self));
		
		return self.Exec(callingEnv, args);
		
	def Exec(self, callingEnv, args):
		raise Exception("Cannot call " + str(self));
	
	def __str__(self):
		return "function(" + ", ".join(self.params) + ")";

class PartialFunction(Function):
	def __init__(self, params, stored, function):
		Function.__init__(self, function.name + "(" + ", ".join(map(str, stored)) + ")", params[len(stored):]);
		self.stored = stored;
		self.function = function;
	
	def Exec(self, callingEnv, args):
		return self.function.Call(callingEnv, self.stored + args);

class PredefinedFunction(Function):
	def __init__(self, name, params, function):
		Function.__init__(self, name, params);
		self.function = function;
	
	def Exec(self, callingEnv, args):
		return self.function(callingEnv, args);

class SwailFunction(Function):
	def __init__(self, name, parentEnv, params, block):
		self.parentEnv = parentEnv;
		self.block = block;
		parameters = [];
		for param in params:
			# make sure we create a new variable and don't overwrite a higher-level one
			parameters.append(param.name.value);
					
		Function.__init__(self, name, parameters);

	def Exec(self, callingEnv, args):
		env = Data.Environment.Environment(self.parentEnv, "<function>");
		i = 0;
		for arg in args:
			env.vars[self.params[i]] = arg;
			i = i + 1;
		
		result = self.block.Evaluate(env);

		return result;