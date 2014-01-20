import sys;

import Data.Function;
import Data.Value;
import Data.Environment;

globalEnv = Data.Environment.Environment(None, "Global");

globalEnv.SetVariable("Global", globalEnv);

globalEnv.SetVariable("true", Data.Value.Bool(True));
globalEnv.SetVariable("false", Data.Value.Bool(False));

def evalFunction(callEnv, args):
	return args[0].Evaluate(callEnv);

globalEnv.SetVariable("~", Data.Function.PredefinedFunction("<lambda>", ["arg"], evalFunction));

def addFunction(callEnv, args):
	return Data.Value.Integer(args[0].value + args[1].value);

globalEnv.SetVariable("add", Data.Function.PredefinedFunction("<lambda>", ["a", "b"], addFunction));

def eqFunction(callEnv, args):
	return Data.Value.Bool(args[0] == args[1]);

globalEnv.SetVariable("eq", Data.Function.PredefinedFunction("<lambda>", ["a", "b"], eqFunction));

def defFunction(callEnv, args):
	callEnv.SetVariable(args[0].name.value, args[1]);
	return args[1];

globalEnv.SetVariable("def", Data.Function.PredefinedFunction("<lambda>", ["name", "variable"], defFunction));

def exitFunction(callEnv, args):
	sys.exit(args[0].value);

globalEnv.SetVariable("exit", Data.Function.PredefinedFunction("<lambda>", ["status"], exitFunction));

def getFunction(callEnv, args):
	return args[0].Access(args[1]);

globalEnv.SetVariable("get", Data.Function.PredefinedFunction("<lambda>", ["object", "name"], getFunction));

def setFunction(callEnv, args):
	return args[0].Set(args[1], args[2]);

globalEnv.SetVariable("set", Data.Function.PredefinedFunction("<lambda>", ["object", "name", "value"], setFunction));

def insertFunction(callEnv, args):
	args[0].Insert(args[1], args[2]);

globalEnv.SetVariable("insert", Data.Function.PredefinedFunction("<lambda>", ["list", "pos", "value"], insertFunction));

def makeFunctionFunction(callEnv, args):
	return Data.Function.SwailFunction("<lambda>", callEnv, args[0].value, args[1]);

globalEnv.SetVariable("function", Data.Function.PredefinedFunction("<lambda>", ["params", "block"], makeFunctionFunction));

def ifFunction(callEnv, args):
	if args[0].value:
		return evalFunction(callEnv, [args[1]]);
	else:
		return evalFunction(callEnv, [args[2]]);

globalEnv.SetVariable("if", Data.Function.PredefinedFunction("<lambda>", ["condition", "then", "else"], ifFunction));

def printFunction(callEnv, args):
	print(str(args[0]));
	
globalEnv.SetVariable("print", Data.Function.PredefinedFunction("<lambda>", ["value"], printFunction));

def typeFunction(callEnv, args):
	return args[0].type;

globalEnv.SetVariable("type", Data.Function.PredefinedFunction("<lambda>", ["object"], typeFunction));

def callFunction(callEnv, args):
	return Data.Lang.FunctionCall("<lambda>", args[0], args[1].value);

globalEnv.SetVariable("call", Data.Function.PredefinedFunction("<lambda>", ["function", "args"], callFunction));

def literalFunction(callEnv, args):
	return Data.Lang.Literal("<literal>", args[0]);

globalEnv.SetVariable("literal", Data.Function.PredefinedFunction("<lambda>", ["value"], literalFunction));

def notFunction(callEnv, args):
	return Data.Value.Bool(not args[0]);

globalEnv.SetVariable("not", Data.Function.PredefinedFunction("<lambda>", ["value"], notFunction));
