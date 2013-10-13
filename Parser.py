# Parser.py - Evaluates source code into instructions

import re;

import Data.Parser;
import ParseEnv;
import Util;

def ParseLine(text,):
	parser = Data.Parser.SubMatch(ParseEnv.parseEnv, "line");
	text, name, result = parser.Match(text);
	if Util.SkipWhitespace(text) != "":
		raise Data.Parser.SyntaxError("Expected <end>, received " + text);
	return result;