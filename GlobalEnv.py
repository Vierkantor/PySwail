import sys;

import Data.Function;
import Data.Value;
import Data.Environment;

globalEnv = Data.Environment.Environment(None, "Global");

globalEnv.SetVariable(Data.Value.Variable("Global"), globalEnv);

globalEnv.SetVariable(Data.Value.Variable("true"), Data.Value.Bool(True));
globalEnv.SetVariable(Data.Value.Variable("false"), Data.Value.Bool(False));

def evalFunction(callEnv, args):
	return args[0].Evaluate(callEnv);

globalEnv.SetVariable(Data.Value.Variable("~"), Data.Function.PredefinedFunction("<lambda>", ["arg"], [], evalFunction));

def addFunction(callEnv, args):
	return Data.Value.Integer(args[0]._value + args[1]._value);

globalEnv.SetVariable(Data.Value.Variable("add"), Data.Function.PredefinedFunction("<lambda>", ["a", "b"], [], addFunction));

def eqFunction(callEnv, args):
	return Data.Value.Bool(args[0] == args[1]);

globalEnv.SetVariable(Data.Value.Variable("eq"), Data.Function.PredefinedFunction("<lambda>", ["a", "b"], [], eqFunction));

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

def notFunction(callEnv, args):
	return Data.Value.Bool(not args[0]);

globalEnv.SetVariable(Data.Value.Variable("not"), Data.Function.PredefinedFunction("<lambda>", ["value"], [], notFunction));
