import re;

import Data.Data;
import Data.Type;

import Util;

parseRuleType = Data.Type.Type("ParseRule");
tokenMatchType = Data.Type.Type("TokenMatch");
literalMatchType = Data.Type.Type("LiteralMatch");
subMatchType = Data.Type.Type("SubMatch");

class SyntaxError (Exception):
	def __init__(self, text, depth):
		self.text = text;
		self.depth = depth;

	def __str__(self):
		return self.text;

class ParseRule(Data.Data.DataValue):
	def __init__(self, name, list, resolver):
		Data.Data.DataValue.__init__(self, parseRuleType, name);
		self.list = list;
		self.resolver = resolver;

	def Evaluate(self, env):
		return self;

	def Match(self, text, env, depth):
		result = {};
		begin = text;
		
		for match in self.list.value:
			text, name, match = match.Match(text, depth);
			depth += len(begin) - len(text);
			result[name] = match;

		return text, self.resolver.Call(env, [Data.Value.Dict(result), Data.Value.String(begin[:len(begin) - len(text)])]);

	def __str__(self):
		return "<<{}>> -> {}".format(self.name, str(self.list));

class Match(Data.Data.DataValue):
	def __init__(self):
		pass;

	def Evaluate(self):
		return self;

class EndMatch(Match):
	def __init__(self):
		Data.Data.DataValue.__init__(self, literalMatchType, "<end>");
	
	def Evaluate(self, env):
		return self;
	
	def Match(self, text, depth):
		text = Util.SkipWhitespace(text);
		if text != '':
			raise SyntaxError("Expected <end>, received " + text, depth);
		
		return text, "end", None;

class TokenMatch(Match):
	def __init__(self):
		Data.Data.DataValue.__init__(self, literalMatchType, "<token>");

	def Evaluate(self, env):
		return self;

	def Match(self, text, depth):
		text = Util.SkipWhitespace(text);
		if text == "" or text[0] == "\n":
			raise SyntaxError("Expected <token>, received <end>.", depth);
		
		# a series of digits is an integer
		match = re.match(r"^(\-?\d+)", text);
		if match != None:
			return text[match.end(1):], "token", Data.Value.Integer(int(match.group(1)));
		
		# a series of letters is a name, those are always literal tokens
		match = re.match(r"^(\w+)", text);
		if match != None:
			return text[match.end(1):], "token", Data.Value.Variable(Data.Value.String(match.group(1)));
		
		# a text with quotes is a string
		if text[0] == '"' or text[0] == "'":
			endChar = text[0];
			contents = [];
			text = text[1:];
			while text[0] != endChar:
				if text[0] == "\\":
					if text[1] == "n":
						contents.append("\n");
					elif text[1] == endChar:
						contents.append(endChar);
					text = text[1:];

				contents.append(text[0]);
				text = text[1:];
				if len(text) == 0:
					raise SyntaxError("String has no end", depth);
			
			text = text[1:];
			return text, "token", Data.Value.String("".join(contents));

		# try to get everything up to the next bit of whitespace
		match = re.match(r"^(.+?)\s|^(.+?)$", text);
		if match != None:
			if match.group(1) == None:
				return text[match.end(2):], "token", Data.Value.Variable(Data.Value.String(match.group(2)));
			else:
				return text[match.end(1):], "token", Data.Value.Variable(Data.Value.String(match.group(1)));
		else:
			raise SyntaxError("Cannot get token from '" + text + "'", depth);

	def __str__(self):
		return "<<token>>";

class LiteralMatch(Match):
	def __init__(self, match):
		Data.Data.DataValue.__init__(self, literalMatchType, '"{}"'.format(match));
		self.match = match;

	def Evaluate(self, env):
		return self;

	def Match(self, text, depth):
		text = Util.SkipWhitespace(text);
		if text[:len(self.match)] == self.match:
			return text[len(self.match):], self.match, self.match;
		else:
			raise SyntaxError("Expected '{}', received '{}'".format(self.match, text), depth);
	
	def __str__(self):
		return "''{}''".format(self.match);

errRule = None;
deepestErr = None;

class SubMatch(Match):
	def __init__(self, env, rule):
		Data.Data.DataValue.__init__(self, subMatchType, "<{}>".format(rule));
		self.env = env;
		self.rule = rule;

	def Evaluate(self, env):
		return self;

	def Match(self, text, depth):
		global maxDepth, errRule, deepestErr;
		
		lastErr = None;
		
		for rule in self.env.GetVariable(self.rule).value:
			try:
				text, result = rule.Match(text, self.env, depth);
				return text, self.rule, result;
			except SyntaxError as e:
				lastErr = e;
				if deepestErr == None or lastErr.depth >= deepestErr.depth:
					deepestErr = SyntaxError("While parsing {}:\n{}".format(self.rule, Util.Indent(str(lastErr))), lastErr.depth);
					errRule = rule;

		if lastErr != None:
			raise SyntaxError("While parsing {}:\n{}".format(self.rule, Util.Indent(str(lastErr))), lastErr.depth);

		raise SyntaxError("No rule defined for <{}>".format(self.rule), depth);

	def __str__(self):
		return "<<{}>>".format(self.rule);
