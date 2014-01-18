# Defines components of the Swail language

import Data.Data;
import Data.Type;

import Util;

newType = Data.Type.Type("New");
blockType = Data.Type.Type("Block");
callType = Data.Type.Type("FunctionCall");
literalType = Data.Type.Type("Literal");

class New(Data.Data.DataValue):
	def __init__(self, name, value):
		Data.Data.DataValue.__init__(self, newType, name);
		self.value = value;

	def Evaluate(self, env):
		self.value.Construct(env);
		return self.value.Evaluate(env);

class Block(Data.Data.DataValue):
	def __init__(self, name, value):
		Data.Data.DataValue.__init__(self, blockType, name);
		self.value = value;
	
	def __str__(self):
		return "{\n  " + "\n  ".join(map(str, self.value)) + "\n}";
	
	def Append(self, value):
		self.value.append(value);
	
	def Insert(self, pos, value):
		self.value.insert(pos.value, value);
	
	def Construct(self, env):
		self.env = Data.Environment.Environment(env, "<block>");
	
	def Evaluate(self, env):
		try:
			result = None;
			for statement in self.value:
				result = statement.Evaluate(self.env);
			return result;
		except Exception as e:
			e = Exception("While evaluating " + str(self.name) + ":\n" + Util.Indent(str(e)));
			raise e;

class FunctionCall(Data.Data.DataValue):
	def __init__(self, name, function, args):
		Data.Data.DataValue.__init__(self, callType, name);
		self.function = function;
		self.args = args;
	
	def Evaluate(self, env):
		args = [x.Evaluate(env) for x in self.args];
		return self.function.Evaluate(env).Call(env, args);
	
	def __str__(self):
		return str(self.function) + "(" + ",".join(map(str, self.args)) + ")";

class Literal(Data.Data.DataValue):
	def __init__(self, name, value):
		Data.Data.DataValue.__init__(self, literalType, name);
		self.value = value;
	
	def Evaluate(self, env):
		return self.value;
	
	def __str__(self):
		return "`(" + str(self.value) + ")";
