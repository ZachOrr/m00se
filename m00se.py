#! /usr/bin/env python

from socket import socket
from redis import StrictRedis
from datetime import datetime
import pickle
from json import dumps, loads
import requests
from deps.hashid import HashChecker
from random import randint
from functools import partial

class InfoMessage(object):
	def __init__(self, name, date, info):
		super(InfoMessage, self).__init__()
		self.name = name
		self.date = date
		self.info = info

class GistException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

class Moose(object):
	def __init__(self, HOST, PORT, NICK):
		super(Moose, self).__init__()
		self.HOST = HOST
		self.PORT = PORT
		self.NICK = NICK
		self.redis_server = StrictRedis(host='127.0.0.1', port=6379, db=0)
		self.irc = socket()
		self.commands = {
			"challs": {
				"number_of_args": 0,
				"text": "!challs - Get all the challenges with info",
				"method": self.challs,
			},
			"add": {
				"number_of_args": -1,
				"username": True,
				"text": "!add [challenge_name OR challenge_id] [url or text] - Add some info to a challenge to help others out",
				"method": self.add,
			},
			"get": {
				"number_of_args": 1,
				"username": True,
				"text": "!get [challenge_name] OR !get #[challenge_id] - Get a gist with all the info for a challenge",
				"method": self.get,
			},
			"calendar": {
				"number_of_args": 0,
				"text": "!calendar - Get the calendar url",
				"method": self.calendar,
			},
			"id": {
				"number_of_args": 1,
				"text": "!id [hash] - Identify a hash",
				"method": self.idhash
			},
			"purge": {
				"number_of_args": 0,
				"username": True,
				"text": "!purge - Remove all challenges (zachzor only)",
				"method": self.purge
			},
			"farts": {
				"number_of_args": 0,
				"text": "!farts - Moose farts",
				"method": self.farts
			},
			"help": {
				"number_of_args": 1,
				"text": "!help [command] - Get info on how to use a command",
				"method": self.help
			},
			"leet": {
				"number_of_args": -1,
				"username": True,
				"text": "!leet [... stuff|(space stuff)] - Increase stuff's leetness",
				"method": self.leet
			},
			"deleet": {
				"number_of_args": -1,
				"username": True,
				"text": "!deleet [... stuff|(space stuff)] - Decrease stuff's leetness",
				"method": self.deleet
			},
			"leets": {
				"number_of_args": -1,
				"text": "!leets [... stuff|(space stuff)] - Display the leetness of stuff",
				"method": self.leets
			},
			"seen": {
				"number_of_args": 1,
				"text": "!seen [username] - Check the last problem someone was working on",
				"method": self.seen
			},
			"github": {
				"number_of_args": 0,
				"text": "!github - Get the github repo url",
				"method": self.github
			}
		}
		f = open("github_oauth_token", "r")
		lines = f.readlines() 
		if len(lines) < 1:
			raise Exception("No token in github_oauth_token!")
		self.headers = {"Authorization": "token %s" % lines[0].strip(), "User-Agent": "ecxinc"}
		f.close()

	def delete_gists(self):
		r = requests.get("https://api.github.com/gists", headers=self.headers)
		for gist in r.json():
			requests.delete("https://api.github.com/gists/%s" % gist["id"], headers=self.headers)

	def create_gist(self, problem_name, problem_info):
		gist = {
			"files": {
				"%s.txt" % problem_name: { 
					"content": "\n".join("[%s %s] %s" % (info.name, info.date, info.info) for info in problem_info)
				}
			},
			"public": False
		}
		r = None
		for g in requests.get("https://api.github.com/gists", headers=self.headers).json():
			if "%s.txt" % problem_name in  g["files"].keys():
				r = requests.patch("https://api.github.com/gists/%s" % g["id"], headers=self.headers, data=dumps(gist))
				break
		if not r:
			r = requests.post("https://api.github.com/gists", headers=self.headers, data=dumps(gist))
		print r.status_code
		if r.status_code != 201 and r.status_code != 200:
			raise GistException("Couldn't create gist!")
		return loads(r.text)["html_url"]

	def connect(self):
		print "Connecting..."
		self.irc.connect((self.HOST, self.PORT))
		self.irc.send("NICK %s\r\n" % self.NICK)
		self.irc.send("USER %s %s bla :%s\r\n" % (self.NICK, self.NICK, self.NICK))
		self.irc.send("JOIN #ctf\r\n")
		print "Connected!"
		self.serve_and_possibly_protect()

	def parsemsg(self, s):
		# Breaks a message from an IRC server into its username, command, and arguments.
		username, trailing = "", []
		if not s:
			return ""
		if s[0] == ':':
			username, s = s[1:].split(' ', 1)
			username_info = username.split("!")
			if len(username_info) > 1:
				username = username_info[0]
		if s.find(' :') != -1:
			s, trailing = s.split(' :', 1)
			args = s.split()
			args.append(trailing.strip().split(" "))
		else:
			args = s.split()
		command = args.pop(0)
		return username, command, args

	def send_message(self, message):
		self.irc.send("PRIVMSG #ctf :%s\r\n" % message)

	def handle_message(self, username, channel, args):
		if len(args) < 1:
			return
		arg = args.pop(0)[1:]
		if arg == "help" and len(args) == 0:
			self.help("")
		elif arg in self.commands.keys():
			arg_num = self.commands[arg]["number_of_args"]
			params = []
			if len(args) < arg_num:
				self.help(arg)
				return
			elif arg_num == 0:
				params = []
			elif arg_num == -1:
				params = [args]
			else:
				params = args[:arg_num]
			if self.commands[arg].get("username", False):
				self.commands[arg]["method"](username, *params)
			else:
				self.commands[arg]["method"](*params)
		elif arg in self.commands.keys():
			self.help(arg)

	def purge(self, username):
		if username == "zachzor":
			self.redis_server.delete("challs")
			self.redis_server.delete("seen")
			self.delete_gists()
			self.send_message("All challenges removed")

	def seen(self, username):
		if not self.redis_server.hexists("seen", username):
			self.send_message("%s was not working on a problem" % username)
		else:
			self.send_message("%s was working on %s" % (username, self.redis_server.hget("seen", username)))

	def update_seen(self, username, challenge_name):
		self.redis_server.hset("seen", username, challenge_name + " | " + datetime.now().strftime("%m-%d-%Y %H:%M:%S"))

	def get(self, username, challenge_name):
		if challenge_name[0] == '#':
			try:
				challenge_number = int(challenge_name[1:])
			except ValueError:
				self.send_message("%s is not a valid challenge id" % challenge_name)
				return
			if self.redis_server.hlen("challs") <= challenge_number or challenge_number < 0:
				self.send_message("%s is not a valid challenge id" % challenge_name)
				return
			else:
				name = [(i, s) for i, s in enumerate(self.redis_server.hkeys("challs"))][challenge_number][1]
				try:
					gist = self.create_gist(name, pickle.loads(self.redis_server.hget("challs", name)))
					self.send_message("%s" % gist)
					self.update_seen(username, challenge_name)
				except GistException:
					self.send_message("Unable to create gist")
		else:
			if not self.redis_server.hexists("challs", challenge_name):
				self.send_message("%s is not a valid challenge name" % challenge_name)
				return
			else:
				try:
					gist = self.create_gist(challenge_name, pickle.loads(self.redis_server.hget("challs", challenge_name)))
					self.send_message("%s" % gist)
					self.update_seen(username, challenge_name)
				except GistException:
					self.send_message("Unable to create gist")

	def farts(self):
		self.send_message(" ".join(list(["pfffttt"] * randint(1, 7))))

	def add(self, username, args):
		if len(args) < 2:
			self.help("add")
			return
		challenge_name, description = args[0], args[1:]
		new_info = InfoMessage(username, datetime.now().strftime("%m-%d-%Y %H:%M:%S"), " ".join(description))
		if self.redis_server.hget("challs", challenge_name) == None:
			self.redis_server.hset("challs", challenge_name, pickle.dumps([new_info]))
		else:
			old = pickle.loads(self.redis_server.hget("challs", challenge_name))
			old.append(new_info)
			self.redis_server.hset("challs", challenge_name, pickle.dumps(old))
		self.send_message("Added!")
		self.update_seen(username, challenge_name)

	@staticmethod
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

	def leetincrby(self, incr, username, args):
		fields = self.parseleetargs(args)
		for field in fields:
			score = self.redis_server.hget("leet", field)
			if not score:
				self.redis_server.hset("leet", field, 0)
			if field == username:
				# Silently deleet on self-leet.
				self.redis_server.hincrby("leet", field, -1)
			else:
				self.redis_server.hincrby("leet", field, incr)

	def leet(self, username, args):
		if len(args) < 1:
			self.help("leet")
		else:
			self.leetincrby(1, username, args)

	def deleet(self, username, args):
		if len(args) < 1:
			self.help("deleet")
		else:
			self.leetincrby(-1, username, args)

	def leets(self, args):
		if len(args) < 1:
			self.help("leets")
			return
		fields = self.parseleetargs(args)
		messages = []
		for field in fields:
			score = self.redis_server.hget("leet", field)
			if not score:
				messages.append("%s isn't leet" % field)
			else:
				messages.append("%s: %s" % (field, score))
		self.send_message(", ".join(messages))

	def idhash(self, hash):
		hash_type = HashChecker(hash)
		hashzor = hash_type.check_hash()
		if hashzor == None:
			self.send_message("Hmm... I'm not sure about that one")
		else:
			self.send_message("That's probably a %s hash" % hashzor)

	def challs(self):
		if self.redis_server.hlen("challs") == 0:
			self.send_message("No challenges")
		else:
			self.send_message("Challenges: %s" % ", ".join(["[%d] %s" % (i, s) for i, s in enumerate(self.redis_server.hkeys("challs"))]))

	def calendar(self):
		self.send_message("http://d.pr/Baur")

	def github(self):
		self.send_message("Fork me at https://github.com/ZachOrr/m00se")

	def help(self, method_name):
		print method_name
		if method_name not in self.commands.keys():
			self.send_message(", ".join(self.commands.keys()))
		else:
			self.send_message(self.commands[method_name]["text"])

	def serve_and_possibly_protect(self):
		while 1:
			data = self.irc.recv(4096)
			username, command, args = self.parsemsg(data)
			if command == "PING":
				self.irc.send("PONG " + data[1] + '\r\n')
			elif command == "PRIVMSG":
				if len(args[1]) > 0 and args[1][0][0] == "!":
					self.handle_message(username, args[0].lower(), [x for x in args[1]])

def main():
	m = Moose("127.0.0.1", 6667, "m00se")
	m.connect()

if __name__ == '__main__':
	main()

# vim: noet:nosta
