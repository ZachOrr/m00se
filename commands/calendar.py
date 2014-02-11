from decorators import command

@command("calendar", argc=0, text="!calendar - Get the calendar url")
def calendar(self):
	self.send_message("http://d.pr/Baur")