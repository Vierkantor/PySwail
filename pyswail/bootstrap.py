"""pyswail.bootstrap - Utilities that allow Python code to produce Swail data,
even when the Swail data depends on this code."""

def returns_bool(function):
	"""Decorator for Python functions that return bools.
	
	Since the boolean type is defined in Swail itself, Python has to look it up to use it.
	"""
	def wrapped(call_env, args): # TODO: make argument list *args
		from Data.Value import Variable
		from GlobalEnv import globalEnv as global_env # TODO: snake_case
		
		false = global_env.GetVariable(Variable("false"))
		true = global_env.GetVariable(Variable("true"))
		if function(call_env, *args):
			return true
		else:
			return false
	
	return wrapped
