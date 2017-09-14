import sys;

import Data.Function;
import Data.Value;
import Data.Struct;

from Data.Environment import Environment
from pyswail.bootstrap import returns_bool
from pyswail.matching import MatchError

globalEnv = Environment(None, "Global")
globalEnv.SetVariable(Data.Value.Variable("Global"), globalEnv);

def evalFunction(callEnv, args):
	return args[0].Evaluate(callEnv);

globalEnv.SetVariable(Data.Value.Variable("~"), Data.Function.PredefinedFunction("<lambda>", ["arg"], [], evalFunction));

def addFunction(callEnv, args):
	return Data.Value.Integer(args[0]._value + args[1]._value);

globalEnv.SetVariable(Data.Value.Variable("add"), Data.Function.PredefinedFunction("<lambda>", ["a", "b"], [], addFunction));

def defFunction(callEnv, args):
	callEnv.SetVariable(args[0], args[1]);
	return args[1];

globalEnv.SetVariable(Data.Value.Variable("def"), Data.Function.PredefinedFunction("<lambda>", ["name", "variable"], [], defFunction));

def exitFunction(callEnv, args):
	sys.exit(args[0]._value);

globalEnv.SetVariable(Data.Value.Variable("exit"), Data.Function.PredefinedFunction("<lambda>", ["status"], [], exitFunction));

def getFunction(callEnv, args):
	return args[0].Get(args[1]);

globalEnv.SetVariable(Data.Value.Variable("get"), Data.Function.PredefinedFunction("<lambda>", ["object", "name"], [], getFunction));

def setFunction(callEnv, args):
	return args[0].Set(args[1], args[2]);

globalEnv.SetVariable(Data.Value.Variable("set"), Data.Function.PredefinedFunction("<lambda>", ["object", "name", "value"], [], setFunction));

def insertFunction(callEnv, args):
	args[0].Insert(args[1], args[2]);

globalEnv.SetVariable(Data.Value.Variable("insert"), Data.Function.PredefinedFunction("<lambda>", ["list", "pos", "value"], [], insertFunction));

def makeFunctionFunction(callEnv, args):
	return Data.Function.SwailFunction("<lambda>", callEnv, args[0], args[1], args[2]);

globalEnv.SetVariable(Data.Value.Variable("function"), Data.Function.PredefinedFunction("<lambda>", ["params", "optionalParams", "block"], [], makeFunctionFunction));

def ifFunction(callEnv, args):
	if bool(args[0]):
		return evalFunction(callEnv, [args[1]]);
	elif len(args) > 2:
		return evalFunction(callEnv, [args[2]]);

globalEnv.SetVariable(Data.Value.Variable("if"), Data.Function.PredefinedFunction("<lambda>", ["condition", "then"], ["else"], ifFunction));

def printFunction(callEnv, args):
	print(str(args[0]));
	
globalEnv.SetVariable(Data.Value.Variable("print"), Data.Function.PredefinedFunction("<lambda>", ["value"], [], printFunction));

def typeFunction(callEnv, args):
	return args[0].type;

globalEnv.SetVariable(Data.Value.Variable("type"), Data.Function.PredefinedFunction("<lambda>", ["object"], [], typeFunction));

def callFunction(callEnv, args):
	return Data.Lang.FunctionCall("<lambda>", args[0], args[1]);

globalEnv.SetVariable(Data.Value.Variable("call"), Data.Function.PredefinedFunction("<lambda>", ["function", "args"], [], callFunction));

def literalFunction(callEnv, args):
	return Data.Lang.Literal("<literal>", args[0]);

globalEnv.SetVariable(Data.Value.Variable("literal"), Data.Function.PredefinedFunction("<lambda>", ["value"], [], literalFunction));

def recordFunction(callEnv, args):
	name = args[0]
	fields = args[1]
	
	return Data.Struct.Record(name, fields, fields)

globalEnv.SetVariable(Data.Value.Variable("record"), Data.Function.PredefinedFunction("<lambda>", ["name", "fields"], [], recordFunction));

def structFunction(callEnv, args):
	records = args[0]
	
	recordDict = {}
	for record in records._value:
		name = record.name._value
		recordDict[name] = record
	
	return Data.Struct.Struct("<struct>", recordDict)

globalEnv.SetVariable(Data.Value.Variable("struct"), Data.Function.PredefinedFunction("<lambda>", ["records"], [], structFunction));

def matchFunction(callEnv, args):
	record, options = args
	
	for option in options:
		pattern, function = option._value
		try:
			bindings = pattern.match(record)
			# TODO: actually bind them
			return function.Call(callEnv, bindings.values())
		except MatchError:
			pass
	
	raise MatchError("incomplete pattern for {}".format(record))

globalEnv.SetVariable(Data.Value.Variable("match"), Data.Function.PredefinedFunction("<lambda>", ["record", "options"], [], matchFunction));

@returns_bool
def is_function(callEnv, lhs, rhs):
	"""Are these two references pointing to the same object?"""
	return lhs == rhs

globalEnv.SetVariable(Data.Value.Variable("is"), Data.Function.PredefinedFunction("<lambda>", ["left", "right"], [], is_function));

def try_function(callEnv, args):
	"""Execute the attempted block until an exception occurs, then execute the reparation block."""
	attempted, reparation = args

	try:
		return attempted.Evaluate(callEnv)
	except Exception as e: # TODO: make this only exceptions raised by Swail
		return reparation.Evaluate(callEnv)

globalEnv.SetVariable(Data.Value.Variable("try"), Data.Function.PredefinedFunction("<lambda>", ["attempted", "reparation"], [], try_function));
