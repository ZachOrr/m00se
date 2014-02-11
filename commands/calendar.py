from decorators import command

@command("calendar", argc=0, text="!calendar - Get the calendar url")
def calendar(moose):
	moose.send_message("http://d.pr/Baur")