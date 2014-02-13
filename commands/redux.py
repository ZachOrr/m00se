from decorators import command

@command("redux", argc=0, text="!redux - Reload commands")
def redux(moose):
	moose.redux()

# vim: noet:nosta
