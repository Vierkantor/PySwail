# Parser.py - Evaluates source code into instructions

import re;

import Data.Parser;
import ParseEnv;
import Util;

def ParseLine(text,):
	Data.Parser.deepestErr = None;
	parser = Data.Parser.SubMatch(ParseEnv.parseEnv, "line");
	try:
		text, name, result = parser.Match(text, 0);
	except Data.Parser.SyntaxError as e:
		raise Data.Parser.deepestErr;
	
	if Util.SkipWhitespace(text) != "":
		raise Data.Parser.SyntaxError("Expected <end>, received " + text, 0);
	return result;
