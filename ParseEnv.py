import Data.Value;
import Data.Parser;

import Data.Environment;
import GlobalEnv;

parseEnv = Data.Environment.Environment(GlobalEnv.globalEnv, "Parser");

parseEnv.SetVariable(Data.Value.Variable("line"), Data.Value.List([
	Data.Parser.ParseRule("line",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "statement"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("statement"))),
	),
	Data.Parser.ParseRule("line",
		Data.Value.List([
			Data.Parser.EndMatch(),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: None),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("block"), Data.Value.List([
	Data.Parser.ParseRule("block",
		Data.Value.List([
			Data.Parser.LiteralMatch("{"),
			Data.Parser.SubMatch(parseEnv, "blockContents"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Lang.New(args[1], args[0].Access(Data.Value.String("blockContents")))),
	),
]), True);

def appendBlock(callEnv, args):
	block = args[0].Access(Data.Value.String("blockContents"));
	block.Insert(Data.Value.Integer(0), args[0].Access(Data.Value.String("statement")));
	block._set("name", args[1]);
	return block;

parseEnv.SetVariable(Data.Value.Variable("blockContents"), Data.Value.List([
	Data.Parser.ParseRule("blockContents",
		Data.Value.List([
			Data.Parser.LiteralMatch("}"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Lang.Block(args[1], [])),
	),
	Data.Parser.ParseRule("blockContents",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "statement"),
			Data.Parser.SubMatch(parseEnv, "blockContents"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], appendBlock),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("statement"), Data.Value.List([
	Data.Parser.ParseRule("statement",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(";"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("expression"))),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("expression"), Data.Value.List([
	Data.Parser.ParseRule("expression",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "call"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("call"))),
	),
	Data.Parser.ParseRule("expression",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "functionable"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("functionable"))),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("call"), Data.Value.List([
	Data.Parser.ParseRule("call",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "functionable"),
			Data.Parser.LiteralMatch("("),
			Data.Parser.SubMatch(parseEnv, "arguments"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Lang.FunctionCall(args[1], args[0].Access(Data.Value.String("functionable")), args[0].Access(Data.Value.String("arguments")))),
	),
]), True);

def appendArgument(callEnv, args):
	list = args[0].Access(Data.Value.String("arguments"));
	list.Insert(Data.Value.Integer(0), args[0].Access(Data.Value.String("expression")));
	list._set("name", args[1]);
	return list;

parseEnv.SetVariable(Data.Value.Variable("arguments"), Data.Value.List([
	Data.Parser.ParseRule("arguments",
		Data.Value.List([
			Data.Parser.LiteralMatch(")"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Value.List([])),
	),
	Data.Parser.ParseRule("arguments",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(")"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Value.List([args[0].Access(Data.Value.String("expression"))])),
	),
	Data.Parser.ParseRule("arguments",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(","),
			Data.Parser.SubMatch(parseEnv, "arguments"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], appendArgument),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("functionable"), Data.Value.List([
	Data.Parser.ParseRule("functionable",
		Data.Value.List([
			Data.Parser.LiteralMatch("("),
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(")"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("expression"))),
	),
	Data.Parser.ParseRule("functionable",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "value"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("value"))),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("value"), Data.Value.List([
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "literal"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("literal"))),
	),
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "block"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("block"))),
	),
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "list"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("list"))),
	),
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "name"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("name"))),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("literal"), Data.Value.List([
	Data.Parser.ParseRule("literal",
		Data.Value.List([
			Data.Parser.LiteralMatch("`"),
			Data.Parser.SubMatch(parseEnv, "functionable"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Lang.Literal(args[1], args[0].Access(Data.Value.String("functionable")))),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("list"), Data.Value.List([
	Data.Parser.ParseRule("list",
		Data.Value.List([
			Data.Parser.LiteralMatch("["),
			Data.Parser.SubMatch(parseEnv, "listElements"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Lang.New(args[1], args[0].Access(Data.Value.String("listElements")))),
	),
]), True);

def appendList(callEnv, args):
	list = args[0].Access(Data.Value.String("listElements"));
	list.Insert(Data.Value.Integer(0), args[0].Access(Data.Value.String("expression")));
	list._set("name", args[1]);
	return list;

parseEnv.SetVariable(Data.Value.Variable("listElements"), Data.Value.List([
	Data.Parser.ParseRule("listElements",
		Data.Value.List([
			Data.Parser.LiteralMatch("]"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Value.List([])),
	),
	Data.Parser.ParseRule("listElements",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch("]"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Value.List([args[0].Access(Data.Value.String("expression"))])),
	),
	Data.Parser.ParseRule("listElements",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(","),
			Data.Parser.SubMatch(parseEnv, "listElements"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], appendList),
	),
]), True);

def insertAccess(callEnv, args):
	list = args[0].Access(Data.Value.String("nameAccess"));
	list.Insert(Data.Value.Integer(0), args[0].Access(Data.Value.String("token")));
	return list;

parseEnv.SetVariable(Data.Value.Variable("nameAccess"), Data.Value.List([
	Data.Parser.ParseRule("name",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "token"),
			Data.Parser.LiteralMatch("."),
			Data.Parser.SubMatch(parseEnv, "nameAccess"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], insertAccess),
	),
	Data.Parser.ParseRule("name",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "token"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: Data.Value.List([args[0].Access(Data.Value.String("token"))])),
	),
]), True);

def resolveAccess(list):
	if len(list) == 0:
		return None;
	elif len(list) == 1:
		return list.Get(Data.Value.Integer(0));
	else:
		return Data.Lang.FunctionCall(
			Data.Value.String("<getter>"),
			Data.Lang.Literal(Data.Value.String("get"), GlobalEnv.globalEnv.GetVariable(Data.Value.Variable("get"))),
			Data.Value.List([
				resolveAccess(Data.Value.List(list._value[:-1])),
				Data.Lang.Literal(list.Get(Data.Value.Integer(-1)), list.Get(Data.Value.Integer(-1)))
			])
		);

parseEnv.SetVariable(Data.Value.Variable("name"), Data.Value.List([
	Data.Parser.ParseRule("name",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "nameAccess"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: resolveAccess(args[0].Access(Data.Value.String("nameAccess")))),
	),
]), True);

def resolveNameSet(list):
	return Data.Value.Dict({
		Data.Value.String("tokenPart"): list.Get(Data.Value.Integer(-1)),
		Data.Value.String("getPart"): resolveAccess(Data.Value.List(list._value[:-1]))
	});

parseEnv.SetVariable(Data.Value.Variable("nameSet"), Data.Value.List([
	Data.Parser.ParseRule("nameSet",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "nameAccess"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: resolveNameSet(args[0].Access(Data.Value.String("nameAccess")))),
	),
]), True);

parseEnv.SetVariable(Data.Value.Variable("token"), Data.Value.List([
	Data.Parser.ParseRule("token",
		Data.Value.List([
			Data.Parser.TokenMatch()
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], [], lambda callEnv, args: args[0].Access(Data.Value.String("token"))),
	),
]), True);

def makeRule(callEnv, args):
	return Data.Parser.ParseRule(args[0]._value, args[1], args[2]);

parseEnv.SetVariable(Data.Value.Variable("rule"), 
	Data.Function.PredefinedFunction("<lambda>", ["name", "matchlist", "resolver"], [], makeRule),
	True
);

def makeLiteralMatch(callEnv, args):
	return Data.Parser.LiteralMatch(args[0]._value);

parseEnv.SetVariable(Data.Value.Variable("literalMatch"), 
	Data.Function.PredefinedFunction("<lambda>", ["text"], [], makeLiteralMatch),
	True
);

def makeSubMatch(callEnv, args):
	if len(args) > 1:
		return Data.Parser.SubMatch(parseEnv, args[0]._value, args[1]._value);
	else:
		return Data.Parser.SubMatch(parseEnv, args[0]._value);

parseEnv.SetVariable(Data.Value.Variable("subMatch"),
	Data.Function.PredefinedFunction("<lambda>", ["rule"], ["name"], makeSubMatch),
	True
);
