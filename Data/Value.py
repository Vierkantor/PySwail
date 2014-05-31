import Data.Data;
import Data.Type;

# basically a name for / reference to other data
variableType = Data.Type.Type("Variable");

class WrappedValue(Data.Data.DataValue):
	def __init__(self, type, value, name = None):
		if name == None:
			name = String(str(value));
		
		Data.Data.DataValue.__init__(self, type, name);
		self._value = value;
	
	def Construct(self, env):
		pass;
	
	def Evaluate(self, env):
		return self;
	
	# equality operators
	def __eq__(self, other):
		if other == None:
			return False;
		
		try:
			return (self._get("type") == other._get("type")) and (self._value == other._value);
		except AttributeError:
			return False;
	
	def __hash__(self):
		return hash(self._value);
	
	# casting operators
	def __bool__(self):
		return bool(self._value);
	
	def __str__(self):
		return str(self._value);
	
	# iterable operators
	def __contains__(self, value):
		return value in self._value;
	
	def __iter__(self):
		return iter(self._value);
	
	def __len__(self):
		return len(self._value);

class Variable(WrappedValue):
	def __init__(self, name):
		try:
			name = name._value;
		except AttributeError:
			pass;
		
		WrappedValue.__init__(self, variableType, name);
	
	def Evaluate(self, env):
		return env.GetVariable(self);

integerType = Data.Type.Type("Integer");

class Integer(WrappedValue):
	def __init__(self, value = 0):
		WrappedValue.__init__(self, integerType, value);

boolType = Data.Type.Type("Bool");

class Bool(WrappedValue):
	def __init__(self, value):
		WrappedValue.__init__(self, boolType, value);

stringType = Data.Type.Type("String");

class String(WrappedValue):
	def __init__(self, value):
		WrappedValue.__init__(self, stringType, value, self);
		
		if type(value) != str:
			raise Exception("{} is not a string!".format(repr(value)));

listType = Data.Type.Type("List");

class List(WrappedValue):
	def __init__(self, value):
		WrappedValue.__init__(self, listType, value);
	
	def Access(self, pos):
		try:
			return self._value[pos._value];
		except (AttributeError, TypeError):
			raise Exception("{} is not a valid index for {}".format(str(pos), str(self)));
	
	def Append(self, value):
		self._value.append(value);
		return self;
	
	def Insert(self, pos, value):
		self._value.insert(pos._value, value);
		return self;
	
	def __str__(self):
		return "[" + ", ".join(map(str, self._value)) + "]";
	
	def Evaluate(self, env):
		result = [];
		for element in self._value:
			result.append(element.Evaluate(env));
		
		return List(result);
	
	def __add__(self, other):
		result = List([]);
		for value in self:
			result.Append(value);
		for value in other:
			result.Append(other);
		return result;

dictType = Data.Type.Type("Dict");

class Dict(WrappedValue):
	def __init__(self, value):
		WrappedValue.__init__(self, dictType, value);
	
	def Access(self, pos):
		try:
			return self._value[pos];
		except KeyError:
			raise Exception("{} is not in {}".format(pos, self));
	
	def Insert(self, pos, value):
		self._value[pos] = value;
	
	def __str__(self):
		return "{" + ", ".join(map(lambda key: repr(key) + ": " + str(self._value[key]), self._value)) + "}";
	
	def Evaluate(self, env):
		result = [];
		for element in self._value:
			result[element.Evaluate(env)] = (self._value[element].Evaluate(env));
		
		return Dict(result);
