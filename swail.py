#!/usr/bin/env python3

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
argparser.add_argument('-i', '--inspect', action='store_const', const=True, default=False, help='Run interactively after executing file.');
argparser.add_argument('file', type=str, default='-', nargs='?', help='The file to run. If "-" or blank, run from stdin.');
args = argparser.parse_args();

def get_lines(source):
	"""Yield double-newline terminated statements from source.
	
	The source should have starting_line and continuing_line methods.
	On EOF, the source should return '' from either method.
	Each line ends with \n, both in the source and in this function.
	Either yields an empty line "\n", or concatenated non-empty lines.
	"""
	while True:
		line = source.starting_line()
		text = []
		while line != '\n':
			if line == '':
				# end of file
				yield "".join(text)
				return
			text.append(line)
			line = source.continuing_line()
		
		yield "".join(text)

class FileSource:
	"""A get_lines-compatible source based on a file object."""
	def __init__(self, source_file):
		self.source_file = source_file
	def starting_line(self):
		return self.source_file.readline()
	def continuing_line(self):
		return self.source_file.readline()
class ReadlineSource:
	"""A get_lines-compatible source using the readline library."""
	def __init__(self):
		self.first_prompt = "> "
		self.continue_prompt = ". "
	def input_line(self, prompt=""):
		"""Read a line from stdin, after asking with a prompt.
		
		Nicely handles the case of EOF by printing a final newline.
		"""
		try:
			return input(prompt) + "\n"
		except EOFError:
			print()
			return ""
	def starting_line(self):
		return self.input_line(self.first_prompt)
	def continuing_line(self):
		return self.input_line(self.continue_prompt)

def RunFile(filename, *, environment=None):
	"""Execute the statements in a file, returning the resulting environment.

	The filename is considered relative to the current working dir.
	If an environment is specified, all definitions are run against that environment.
	If not specified, a new one is made, child of the global environment.
	"""
	if not environment:
		environment = Data.Environment.Environment(GlobalEnv.globalEnv, filename)
	
	with open(filename, 'r') as file:
		for statement in get_lines(FileSource(file)):
			if statement == '\n':
				continue
			try:
				parsed = Parser.ParseLine(statement);
				if parsed is not None:
					parsed.Evaluate(environment);
			except Exception as e:
				print("At " + statement);
				print(Util.Indent(str(e)));
				raise e;
	
	return environment

# execute the stdlib
if not args.nostd:
	RunFile("stdlib.swa", environment=GlobalEnv.globalEnv)

if args.file != '-':
	RunFile(args.file, environment=inputEnv);

if args.file == '-' or args.inspect:
	# do the read-parse-execute loop
	for text in get_lines(ReadlineSource()):
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
			if parsed is not None:
				result = parsed.Evaluate(inputEnv);
				if result is not None:
					print(result);
		except Exception as e:
			if args.verbose:
				print("Full stack trace:");
				traceback.print_exc();
			else:
				print(str(e));
			continue;
