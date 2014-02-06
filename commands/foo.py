'''Defines the foo command.'''

from decorators import command

@command("foo", number_of_args=0, text="foo", username=True)
def foo(moose, username):
    '''Print foo.'''
	moose.send_message(username + " foo")

