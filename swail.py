#!/usr/bin/python3

from argparse import ArgumentParser;
import atexit;
import os;
import readline;
import traceback;
import sys;

import Data;
import Data.Environment;
import GlobalEnv;
import Parser;
import Util;

inputEnv = Data.Environment.Environment(GlobalEnv.globalEnv, "<input>");

# some constants
name = 'PySwail';
version = '0.02';

histfile = os.path.join(os.path.expanduser("~"), ".swa_history")
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, histfile)

# parse the command line arguments
argparser = ArgumentParser(description = "The Python interpreter for Swail", prog="PySwail");
argparser.add_argument('-S', '--nostd', dest='nostd', action='store_const', const=True, default=False, help='Do not load the standard library before running input');
argparser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True, default=False, help='Show full stack trace when encountering exceptions');
argparser.add_argument('-V', '--version', action='version', version='%(prog)s ' + version);
args = argparser.parse_args();

# execute the stdlib
if not args.nostd:
	with open('stdlib.swa', 'r') as stdlibFile:
		line = stdlibFile.readline();
		while line != '':
			newLine = "<empty>";
			while newLine != "" and newLine != "\n":
				newLine = stdlibFile.readline();
				line = line + newLine;
			if len(line) > 1:
				try:
					parsed = Parser.ParseLine(line);
					if parsed != None:
						parsed.Evaluate(inputEnv);
				except Exception as e:
					print("At " + line);
					print(Util.Indent(str(e)));
					raise e;
			line = stdlibFile.readline();

# do the read-parse-execute loop
while True:
	try:
		text = input("> ");
		while text != "" and text[-1:] != "\n":
			text = text + "\n" + input(". ");
	except EOFError as e:
		print("");
		break;
	
	try:
		parsed = Parser.ParseLine(text);
	except Exception as e:
		print("Exception while parsing <input>:");
		if args.verbose:
			print("Full stack trace:");
			traceback.print_exc();
		else:
			print(Util.Indent(str(e)));
		continue;
	
	try:
		if parsed != None:
			print(parsed.Evaluate(inputEnv));
	except Exception as e:
		if args.verbose:
			print("Full stack trace:");
			traceback.print_exc();
		else:
			print(str(e));
		continue;