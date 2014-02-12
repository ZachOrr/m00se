from decorators import command
import requests

@command("purge", argc=0, text="!purge - Remove all challenges (zachzor only)", username=True)
def purge(moose, username):
	if username == "zachzor":
		moose.redis_server.delete("challs")
		moose.redis_server.delete("seen")
		delete_gists(moose)
		moose.send_message("All challenges removed")

def delete_gists(moose):
	r = requests.get("https://api.github.com/gists", headers=moose.headers)
	for gist in r.json():
		requests.delete("https://api.github.com/gists/%s" % gist["id"], headers=moose.headers)
