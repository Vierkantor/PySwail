import Data.Type

recordType = Data.Type.Type("Record");
class Record(Data.Function.Function):
	def __init__(self, name, fields, values):
		Data.Function.Function.__init__(self, name, fields, [])
		self._set("type", self)
		
		self.name = name
		self.fields = fields
		self.values = values
	
	def Exec(self, callingEnv, args):
		record = Record(self.name, self.fields, args)
		record._set("type", self._get("type"))
		
		return record
	
	def __str__(self):
		return "{}({})".format(self.name, ", ".join(map(str, self.values)))

structType = Data.Type.Type("Struct");
Data.Type.typeType.AddSubtype(structType);
class Struct(Data.Type.Type):
	""" A data structure """
	def __init__(self, name, records):
		Data.Data.DataValue.__init__(self, structType, name)
		
		self.records = records
	
	def Access(self, name):
		try:
			return self.records[name._value]
		except KeyError:
			raise Exception("Invalid record {}".format(str(name)))
	
	def __str__(self):
		return "struct {} [{}]".format(self._get("name"), ", ".join(map(str, self.records)))
