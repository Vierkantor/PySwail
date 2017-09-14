"""pyswail.matching - Utilities for the unification process of the `match function.

Unification is handled by calling pattern.match(value),
which either returns a dictionary of variable assignments to make this true,
or raises a MatchError.
"""

class MatchError(Exception):
	"""Raised when a pattern does not match the value."""
	pass
