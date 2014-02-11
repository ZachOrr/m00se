from decorators import command
from deps.helpers import leetincrby

@command("deleet", argc=-1, text="!deleet [... stuff|(space stuff)] - Decrease stuff's leetness", username=True)
def deleet(moose, username, args):
	if len(args) < 1:
		moose.cmd("help", "deleet")
	else:
		leetincrby(moose, -1, username, args)
