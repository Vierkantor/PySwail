import Data.Data;
import Data.Type;

# basically a name for / reference to other data
variableType = Data.Type.Type("Variable");

class Variable(Data.Data.DataValue):
	def __init__(self, name):
		Data.Data.DataValue.__init__(self, variableType, name);
	
	def Evaluate(self, env):
		return env.GetVariable(self.name.value);
	
	def __str__(self):
		return str(self.name.value);

integerType = Data.Type.Type("Integer");

class Integer(Data.Data.DataValue):
	def __init__(self, value = 0):
		Data.Data.DataValue.__init__(self, integerType, str(value));
		self.value = value;
	
	def __str__(self):
		return str(self.value);
	
	def Evaluate(self, env):
		return self;

boolType = Data.Type.Type("Bool");

class Bool(Data.Data.DataValue):
	def __init__(self, value):
		Data.Data.DataValue.__init__(self, boolType, str(value));
		self.value = value;
	
	def __str__(self):
		return str(self.value);
	
	def Evaluate(self, env):
		return self;

stringType = Data.Type.Type("String");

class String(Data.Data.DataValue):
	def __init__(self, value):
		Data.Data.DataValue.__init__(self, stringType, '"' + str(value) + '"');
		self.value = value;
	
	def __str__(self):
		return '"' + str(self.value) + '"';
	
	def Evaluate(self, env):
		return self;

listType = Data.Type.Type("List");

class List(Data.Data.DataValue):
	def __init__(self, value):
		Data.Data.DataValue.__init__(self, listType, str(value));
		self.value = value;

	def Append(self, value):
		self.value.append(value);

	def Insert(self, pos, value):
		self.value.insert(pos.value, value);

	def __str__(self):
		return "[" + ", ".join(map(str, self.value)) + "]";
	
	def __getitem__(self, key):
		return self.value[key];

	def Construct(self, env):
		pass;

	def Evaluate(self, env):
		result = [];
		for element in self.value:
			result.append(element.Evaluate(env));

		return List(result);

dictType = Data.Type.Type("Dict");

class Dict(Data.Data.DataValue):
	def __init__(self, value):
		Data.Data.DataValue.__init__(self, dictType, str(value));
		self.value = value;

	def Access(self, pos):
		return self.Get(pos.value);

	def Set(self, pos, value):
		self.Insert(pos.value, value);

	def Get(self, pos):
		return self.value[pos];

	def Insert(self, pos, value):
		self.value[pos] = value;

	def __str__(self):
		return "{" + ", ".join(map(str, self.value)) + "]";

	def __getitem__(self, key):
		return self.value[key];

	def Evaluate(self, env):
		result = [];
		for element in self.value:
			result[element.Evaluate(env)] = (self.value[element].Evaluate(env));

		return Dict(result);
	