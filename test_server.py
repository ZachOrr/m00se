# test_server.py

import socket
import select
from time import sleep

def main():
	s = socket.socket()
	s.settimeout(10)
	s.bind(("127.0.0.1", 6667))
	s.listen(1)
	c, addr = s.accept()
	while True:
		sleep(0.5)
		while True:
			try:
				q = c.recv(4096)
				print q
			except:
				break
		command = raw_input("Command: ")
		if len(command) > 0 and command[0] == "!":
			c.send(":zachzor!zachzor@yakko.cs.wmich.edu PRIVMSG #ctf :%s" % command)

if __name__ == '__main__':
	main()