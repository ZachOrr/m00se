from decorators import command

@command("seen", argc=1, text="!seen [username] - Check the last problem someone was working on")
def seen(moose, username):
	if not moose.redis_server.hexists("seen", username):
		moose.send_message("%s was not working on a problem" % username)
	else:
		moose.send_message("%s was working on %s" % (username, moose.redis_server.hget("seen", username)))