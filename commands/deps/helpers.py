from datetime import datetime

def parseleetargs(args):
	'''Parse a list of strings, grouping (parenthetical captures).'''
	# Whether we are in a (...) capture; note that these do not nest.
	capturing = False
	fields = []
	for arg in args:
		clean = arg.lstrip("(").rstrip(")")
		if capturing:
			# Capturing, so append arg to end of previous one.
			fields[-1] += " " + clean
			# Continue capturing if this arg doesn't end the capture.
			capturing = not arg.endswith(")")
		else:
			# Not capturing, just append to list.
			fields.append(clean)
			# Start capturing if arg begins a capture and doesn't end it.
			capturing = arg.startswith("(") and not arg.endswith(")")
	return fields

def leetincrby(moose, incr, username, args):
	fields = parseleetargs(args)
	for field in fields:
		score = moose.redis_server.hget("leet", field)
		if not score:
			moose.redis_server.hset("leet", field, 0)
		if field == username:
			# Silently deleet on self-leet.
			moose.redis_server.hincrby("leet", field, -1)
		else:
			moose.redis_server.hincrby("leet", field, incr)

def update_seen(moose, username, challenge_name):
	moose.redis_server.hset("seen", username, challenge_name + " | " + datetime.now().strftime("%m-%d-%Y %H:%M:%S"))