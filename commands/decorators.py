'''Defines convenience function decorators for registering commands.'''

from registry import register

def command(name, **options):
	'''Decorator for m00se command functions.

	Example usage:

	@decorator("foo_cmd", number_of_args=0, text="foo")
	def foo_cmd(moose):
		moose.send_message("foo")

	'''
	def decorator(f):
		options['method'] = f
		register(name, options)
		return f
	return decorator

# vim: noet:nosta
