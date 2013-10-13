# Util.py - Defines some handy tools

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
		else:
			break;
	return string;