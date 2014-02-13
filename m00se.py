#! /usr/bin/env python

from socket import socket
from redis import StrictRedis
from datetime import datetime
from functools import partial
import commands
from commands import registry
import sys

class Moose(object):

	def __init__(self, HOST, PORT, NICK, CHANNEL):
		super(Moose, self).__init__()
		self.HOST = HOST
		self.PORT = PORT
		self.NICK = NICK
		self.CHANNEL = CHANNEL
		self.redis_server = StrictRedis(host='127.0.0.1', port=6379, db=0)
		self.irc = socket()
		# Pull in commands defined in package `commands`.
		self.redux()
		f = open("github_oauth_token", "r")
		lines = f.readlines() 
		if len(lines) < 1:
		  raise Exception("No token in github_oauth_token!")
		self.headers = {"Authorization": "token %s" % lines[0].strip(), "User-Agent": "ecxinc"}
		f.close()

	def connect(self):
		print "Connecting..."
		self.irc.connect((self.HOST, self.PORT))
		self.irc.send("NICK %s\r\n" % self.NICK)
		self.irc.send("USER %s %s bla :%s\r\n" % (self.NICK, self.NICK, self.NICK))
		self.irc.send("JOIN #%s\r\n" % self.CHANNEL)
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
		self.irc.send("PRIVMSG #%s :%s\r\n" % (self.CHANNEL, message))

	def handle_message(self, username, channel, args):
		if len(args) < 1:
			return
		arg = args.pop(0)[1:]
		# boolean waterslide
		if arg == "help" and len(args) == 0:
			self.cmd("help", "")
		elif arg in self.commands.keys():
			arg_num = self.commands[arg]["argc"]
			params = []
			if len(args) < arg_num:
				self.cmd("help", arg)
				return
			elif arg_num == 0:
				params = []
			elif arg_num == -1:
				params = [args]
			else:
				params = args[:arg_num]
			if self.commands[arg].get("username", False):
				self.cmd(arg, username, *params)
			else:
				self.cmd(arg, *params)

	def cmd(self, name, *args):
		self.commands[name]['method'](self, *args)

	def redux(self):
		# Get new __all__; we have to reinvent the wheel because `from package
		# import *` syntax only works at package level and not dynamically.
		reload(commands)
		# Reload registry
		reload(commands.registry)
		# Import or reload
		for command in commands.__all__:
			if 'commands.' + command in sys.modules and sys.modules['commands.' + command]:
				try:
					reload(sys.modules['commands.' + command])
				except ImportError, e:
					self.send_message('Unable to reload command: ' + str(e))
			else:
				try:
					__import__('commands', globals(), locals(), fromlist=[command])
				except ImportError, e:
					self.send_message('Unable to load command: ' + str(e))
		self.commands = registry.commands

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
	m = Moose("127.0.0.1", 6667, "m00se-bots", "bots")
	m.connect()

if __name__ == '__main__':
	main()

# vim: noet:nosta
