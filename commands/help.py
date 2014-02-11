from decorators import command

@command("help", argc=1, text="!help [command] - Get info on how to use a command")
def help(moose, method_name):
	if method_name not in moose.commands.keys():
		moose.send_message(", ".join(moose.commands.keys()))
	else:
		moose.send_message(moose.commands[method_name]["text"])