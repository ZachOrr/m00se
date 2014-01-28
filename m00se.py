# m00se.py

from socket import socket
from redis import StrictRedis
import requests
from datetime import datetime
import json
import pickle

"""
> r.get("challs")
=> {
	"botnet": [
		{"name": "zachzor", "date": "1-26-2014 18:00:19", "info": "Use JS to send commands in panel"},
		{"name": "zachzor", "date": "1-27-2014 02:03:29", "info": "We need to do DNS tunneling"}
	],
	"web_100": [
		{"name": "mandatory", "date": "1-27-2014 02:03:29", "info": "Weird. This may be difficult... I'll come back later"}
	]
}
"""

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
		self.r = StrictRedis(host='127.0.0.1', port=6379, db=0)
		self.irc = socket()
		self.commands = {
			"challs": {
				"text": "!challs - Get all the challenges with info",
				"method": self.challs,
			},
			"add": {
				"text": "!add [challenge_name OR challenge_id] [url or text] - Add some info to a challenge to help others out",
				"method": self.add,
			},
			"get": {
				"text": "!get [challenge_name OR challenge_id] - Get a gist with all the info for a challenge",
				"method": self.get,
			},
			"calendar": {
				"text": "!calendar - Get the calendar url",
				"method": self.calendar,
			},
			"purge": {
				"text": "!purge - Remove all challenges (zachzor only)",
				"method": self.purge
			},
			"help": {
				"text": "!help [command] - Get info on how to use a command",
				"method": self.help
			},
		}
		f = open("github_oauth_token", "r")
		lines = f.readlines() 
		if len(lines) < 1:
			raise Exception("No token in github_oauth_token!")
		self.headers = {'Authorization': 'token %s' % lines[0], 'User-Agent':'ecxinc', 'Content-Type': 'application/json'}
		f.close()

	def create_gist(self, problem_name, problem_info):
		gist = {
			"description": "the description for this gist",
			"public": False,
			"files": {
				"%s.txt" % problem_name: {
					"content": "\n".join("[%s %s] %s" % (info.name, info.date, info.info) for info in problem_info)
				}
			}
		}
		body = json.dumps(gist)
		r = requests.post("https://api.github.com/gists", data=body, headers=self.headers)
		print r.text
		if r.status_code != 201:
			raise GistException("Couldn't create gist!")
		return r["html_url"]

	def connect(self):
		self.irc.connect((self.HOST, self.PORT))
		self.irc.send("NICK %s\r\n" % self.NICK)
		self.irc.send("USER %s %s bla :%s\r\n" % (self.NICK, self.NICK, self.NICK))
		self.irc.send("JOIN #bottest\r\n")
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

	def send_message(self, channel, message):
		self.irc.send("PRIVMSG %s :%s\r\n" % (channel, message))

	def handle_message(self, username, channel, args):
		print args
		if len(args) < 1:
			return
		arg = args[0][1:]
		if arg in self.commands.keys():
			self.commands[arg]["method"](username, channel, args[1:])

	def purge(self, username, channel, args):
		if username == "zachzor":
			self.r.delete("challs")
			self.send_message(channel, "All challenges removed")

	def get(self, username, channel, args):
		if len(args) < 1:
			self.help(username, channel, ["get"])
			return
		if self.r.hexists("challs", args[0]) == False:
			self.send_message(channel, "%s is not a challenge" % args[0])
			return
		try:
			gist = self.create_gist(args[0], pickle.loads(self.r.hget("challs", args[0])))
			self.send_message(channel, "%s: %s" % (username, gist))
		except GistException, e:
			self.send_message(channel, "%s: Unable to create gist" % username)

	def add(self, username, channel, args):
		if len(args) < 2:
			self.help(username, channel, ["add"])
			return
		new_info = InfoMessage(username, datetime.now().strftime("%m-%d-%Y %H:%M:%S"), " ".join(args[1:]))
		if self.r.hget("challs", args[0]) == None:
			self.r.hset("challs", args[0], pickle.dumps([new_info]))
		else:
			old = pickle.loads(self.r.hget("challs", args[0]))
			old.append(new_info)
			self.r.hset("challs", args[0], pickle.dumps(old))
		self.send_message(channel, "%s: Added!" % username)

	def challs(self, username, channel, args):
		if self.r.hlen("challs") == 0:
			self.send_message(channel, "No challenges")
		else:
			self.send_message(channel, "Challenges: %s" % ", ".join(["[%d] %s" % (i, s) for i, s in enumerate(self.r.hkeys("challs"))]))

	def calendar(self, username, channel, args):
		self.send_message(channel, "%s: http://d.pr/Baur" % username)

	def help(self, username, channel, args):
		if len(args) == 0 or args[0] not in self.commands.keys():
			self.send_message(channel, ", ".join(self.commands.keys()))
		else:
			self.send_message(channel, self.commands[args[0]]["text"])

	def serve_and_possibly_protect(self):
		while 1:
			data = self.irc.recv(4096)
			username, command, args = self.parsemsg(data)
			if command == "PING":
				self.irc.send("PONG " + data[1] + '\r\n' )
			elif command == "PRIVMSG":
				if len(args[1]) > 0 and args[1][0][0] == "!":
					self.handle_message(username, args[0], [x.lower() for x in args[1]])

def main():
	m = Moose("127.0.0.1", 6667, "m00se")
	m.connect()

if __name__ == '__main__':
	main()