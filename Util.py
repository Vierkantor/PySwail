# Util.py - Defines some handy tools

class ParseError(Exception):
	pass

# adds two spaces in front of every line
def Indent(string):
	return "  " + "\n  ".join(string.splitlines());

# returns the string from the next non-whitespace or comment character
def SkipWhitespace(string):
	while len(string) > 0:
		if string[0] == " " or string[0] == "\t" or string[0] == "\n":
			string = string[1:];
		elif string[0:2] == "//":
			while len(string) > 0 and string[0] != "\n":
				string = string[1:];
		elif string[0:2] == "/*":
			string = string[2:]
			depth = 1
			while depth > 0:
				if len(string) <= 0:
					raise ParseError("unclosed comment")
				if string[0:2] == "*/":
					depth -= 1
					string = string[2:]
				elif string[0:2] == "/*":
					depth += 1
					string = string[2:]
				else:
					string = string[1:];
		else:
			break;
	return string;
