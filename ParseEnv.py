import Data.Value;
import Data.Parser;

import Data.Environment;
import GlobalEnv;

parseEnv = Data.Environment.Environment(GlobalEnv.globalEnv, "Parser");

parseEnv.SetVariable("line", Data.Value.List([
	Data.Parser.ParseRule("line",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "statement"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("statement")),
	),
	Data.Parser.ParseRule("line",
		Data.Value.List([
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: None),
	),
]), True);

parseEnv.SetVariable("block", Data.Value.List([
	Data.Parser.ParseRule("block",
		Data.Value.List([
			Data.Parser.LiteralMatch("{"),
			Data.Parser.SubMatch(parseEnv, "blockContents"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Lang.New(args[1], args[0].Get("blockContents"))),
	),
]), True);

def appendBlock(callEnv, args):
	block = args[0].Get("blockContents");
	block.Insert(Data.Value.Integer(0), args[0].Get("statement"));
	block.name = args[1];
	return block;

parseEnv.SetVariable("blockContents", Data.Value.List([
	Data.Parser.ParseRule("blockContents",
		Data.Value.List([
			Data.Parser.LiteralMatch("}"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Lang.Block(args[1], [])),
	),
	Data.Parser.ParseRule("blockContents",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "statement"),
			Data.Parser.SubMatch(parseEnv, "blockContents"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], appendBlock),
	),
]), True);

parseEnv.SetVariable("statement", Data.Value.List([
	Data.Parser.ParseRule("statement",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(";"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("expression")),
	),
]), True);

parseEnv.SetVariable("expression", Data.Value.List([
	Data.Parser.ParseRule("expression",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "call"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("call")),
	),
	Data.Parser.ParseRule("expression",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "functionable"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("functionable")),
	),
]), True);

parseEnv.SetVariable("call", Data.Value.List([
	Data.Parser.ParseRule("call",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "functionable"),
			Data.Parser.LiteralMatch("("),
			Data.Parser.SubMatch(parseEnv, "arguments"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Lang.FunctionCall(args[1], args[0].Get("functionable"), args[0].Get("arguments"))),
	),
]), True);

def appendArgument(callEnv, args):
	list = args[0].Get("arguments");
	list.Insert(Data.Value.Integer(0), args[0].Get("expression"));
	list.name = args[1];
	return list;

parseEnv.SetVariable("arguments", Data.Value.List([
	Data.Parser.ParseRule("arguments",
		Data.Value.List([
			Data.Parser.LiteralMatch(")"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Value.List([])),
	),
	Data.Parser.ParseRule("arguments",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(")"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Value.List([args[0].Get("expression")])),
	),
	Data.Parser.ParseRule("arguments",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(","),
			Data.Parser.SubMatch(parseEnv, "arguments"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], appendArgument),
	),
]), True);

parseEnv.SetVariable("functionable", Data.Value.List([
	Data.Parser.ParseRule("functionable",
		Data.Value.List([
			Data.Parser.LiteralMatch("("),
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(")"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("expression")),
	),
	Data.Parser.ParseRule("functionable",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "value"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("value")),
	),
]), True);

parseEnv.SetVariable("value", Data.Value.List([
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "literal"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("literal")),
	),
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "block"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("block")),
	),
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "list"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("list")),
	),
	Data.Parser.ParseRule("value",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "name"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("name")),
	),
]), True);

parseEnv.SetVariable("literal", Data.Value.List([
	Data.Parser.ParseRule("literal",
		Data.Value.List([
			Data.Parser.LiteralMatch("`"),
			Data.Parser.SubMatch(parseEnv, "functionable"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Lang.Literal(args[1], args[0].Get("functionable"))),
	),
]), True);

parseEnv.SetVariable("list", Data.Value.List([
	Data.Parser.ParseRule("list",
		Data.Value.List([
			Data.Parser.LiteralMatch("["),
			Data.Parser.SubMatch(parseEnv, "listElements"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Lang.New(args[1], args[0].Get("listElements"))),
	),
]), True);

def appendList(callEnv, args):
	list = args[0].Get("listElements");
	list.Insert(Data.Value.Integer(0), args[0].Get("expression"));
	list.name = args[1];
	return list;

parseEnv.SetVariable("listElements", Data.Value.List([
	Data.Parser.ParseRule("listElements",
		Data.Value.List([
			Data.Parser.LiteralMatch("]"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Value.List([])),
	),
	Data.Parser.ParseRule("listElements",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch("]"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Value.List([args[0].Get("expression")])),
	),
	Data.Parser.ParseRule("listElements",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "expression"),
			Data.Parser.LiteralMatch(","),
			Data.Parser.SubMatch(parseEnv, "listElements"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], appendList),
	),
]), True);

def insertAccess(callEnv, args):
	list = args[0].Get("nameAccess");
	list.Insert(Data.Value.Integer(0), args[0].Get("token"));
	return list;

parseEnv.SetVariable("nameAccess", Data.Value.List([
	Data.Parser.ParseRule("name",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "token"),
			Data.Parser.LiteralMatch("."),
			Data.Parser.SubMatch(parseEnv, "nameAccess"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], insertAccess),
	),
	Data.Parser.ParseRule("name",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "token"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: Data.Value.List([args[0].Get("token")])),
	),
]), True);

def resolveAccess(list):
	if len(list.value) == 1:
		return list.Get(0);
	else:
		return Data.Lang.FunctionCall(
			"<getter>",
			Data.Lang.Literal("get", GlobalEnv.globalEnv.GetVariable("get")),	
			Data.Value.List([
				resolveAccess(Data.Value.List(list.value[:-1])),
				Data.Lang.Literal(list.Get(-1).name, list.Get(-1))
			])
		);

parseEnv.SetVariable("name", Data.Value.List([
	Data.Parser.ParseRule("name",
		Data.Value.List([
			Data.Parser.SubMatch(parseEnv, "nameAccess"),
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: resolveAccess(args[0].Get("nameAccess"))),
	),
]), True);

parseEnv.SetVariable("token", Data.Value.List([
	Data.Parser.ParseRule("token",
		Data.Value.List([
			Data.Parser.TokenMatch()
		]),
		Data.Function.PredefinedFunction('<lambda>', ['parsed', 'text'], lambda callEnv, args: args[0].Get("token")),
	),
]), True);

def makeRule(callEnv, args):
	return Data.Parser.ParseRule(args[0].value, args[1], args[2]);

parseEnv.SetVariable("rule", 
	Data.Function.PredefinedFunction("<lambda>", ["name", "matchlist", "resolver"], makeRule),
	True
);

def makeLiteralMatch(callEnv, args):
	return Data.Parser.LiteralMatch(args[0].value);

parseEnv.SetVariable("literalMatch", 
	Data.Function.PredefinedFunction("<lambda>", ["text"], makeLiteralMatch),
	True
);

def makeSubMatch(callEnv, args):
	return Data.Parser.SubMatch(parseEnv, args[0].value);

parseEnv.SetVariable("subMatch", 
	Data.Function.PredefinedFunction("<lambda>", ["rule"], makeSubMatch),
	True
);