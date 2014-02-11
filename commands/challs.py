from decorators import command

@command("challs", argc=0, text="!challs - Get all the challenges with info")
def challs(moose):
	if moose.redis_server.hlen("challs") == 0:
		moose.send_message("No challenges")
	else:
		moose.send_message("Challenges: %s" % ", ".join(["[%d] %s" % (i, s) for i, s in enumerate(moose.redis_server.hkeys("challs"))]))