from decorators import command

@command("github", argc=0, text="!github - Get the github repo url")
def github(moose):
	moose.send_message("Fork me at https://github.com/ZachOrr/m00se")