from decorators import command
from deps.helpers import leetincrby

@command("get", argc=-1, text="!leet [... stuff|(space stuff)] - Increase stuff's leetness", username=True)
def leet(moose, username, args):
	if len(args) < 1:
		moose.cmd("help", "leet")
	else:
		leetincrby(moose, 1, username, args)
