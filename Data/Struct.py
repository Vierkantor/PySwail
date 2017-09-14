import Data.Type
import Data.Value

from pyswail.matching import MatchError

recordType = Data.Type.Type("Record");
class Record(Data.Function.Function):
	def __init__(self, name, fields, values):
		Data.Function.Function.__init__(self, name, fields, [])
		self._set("type", recordType)
		self._set("parent_record", self)
		
		self.name = name
		self.fields = fields
		self.values = values
	
	def Exec(self, callingEnv, args):
		record = Record(self.name, self.fields, Data.Value.List(args))
		record._set("parent_record", self._get("parent_record"))
		
		return record

	def match(self, other):
		"""Determine whether the other record is an instance of this one.
		
		See also pyswail.matching for more information about this interface.
		"""
		# if this record is supposed to be abstract, compare by types
		if self._get("parent_record") is self:
			if other._get("parent_record") is self:
				return {}
		
		# both are supposed to be instances, also compare by values
		if self._get("parent_record") is other._get("parent_record"):
			if self.values == other.values:
				return {}
		
		raise MatchError("could not unify {} with {}".format(self, other))
	
	def __str__(self):
		return "record {}({})".format(self.name, ", ".join(map(str, self.values)))

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
