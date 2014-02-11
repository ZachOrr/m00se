from decorators import command
from deps.hashid import HashChecker

@command("id", argc=1, text="!id [hash] - Identify a hash")
def idhash(moose, hash):
	hash_type = HashChecker(hash)
	hashzor = hash_type.check_hash()
	if hashzor == None:
		moose.send_message("Hmm... I'm not sure about that one")
	else:
		moose.send_message("That's probably a %s hash" % hashzor)
