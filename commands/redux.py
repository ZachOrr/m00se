from decorators import command

@command("redux", argc=0, text="!redux - Reload commands")
def redux(moose):
	moose.redux()
	moose.send_message("Commands reloaded!")

# vim: noet:nosta
