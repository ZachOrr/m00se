from decorators import command
from deps import InfoMessage
from datetime import datetime
from deps.helpers import update_seen
from pickle import dumps, loads

@command("add", argc=-1, text="!add [challenge_name OR challenge_id] [url or text] - Add some info to a challenge to help others out", username=True)
def add(moose, username, args):
	if len(args) < 2:
		moose.cmd("help", "add")
		return
	challenge_name, description = args[0], args[1:]
	new_info = InfoMessage(username, datetime.now().strftime("%m-%d-%Y %H:%M:%S"), " ".join(description))
	if moose.redis_server.hget("challs", challenge_name) == None:
		moose.redis_server.hset("challs", challenge_name, dumps([new_info]))
	else:
		old = loads(moose.redis_server.hget("challs", challenge_name))
		old.append(new_info)
		moose.redis_server.hset("challs", challenge_name, dumps(old))
	moose.send_message("Added!")
	update_seen(moose, username, challenge_name)
