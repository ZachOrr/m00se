from decorators import command
from deps.helpers import parseleetargs

@command("leets", argc=-1, text="!leets [... stuff|(space stuff)] - Display the leetness of stuff")
def leets(moose, args):
	if len(args) < 1:
		moose.cmd("help", "leets")
		return
	fields = parseleetargs(args)
	messages = []
	for field in fields:
		score = moose.redis_server.hget("leet", field)
		if not score:
			messages.append("%s isn't leet" % field)
		else:
			messages.append("%s: %s" % (field, score))
	moose.send_message(", ".join(messages))
