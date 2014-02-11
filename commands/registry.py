'''Maintains a dict of registered commands.'''

# Global registration dict for commands.
commands = {}

def register(name, options):
    '''Register a command.'''
    global registered
    commands[name] = options

# vim: noet:nosta
