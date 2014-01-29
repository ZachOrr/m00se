# m00se

ECX Inc's IRC bot - used to save information (links, snippets, etc) on challenges we're working on so others can view them. Maybe we'll make it do some more cool things

## Seting Up

You'll need some dependicies. First, make sure you have virtualenv installed so we can sandbox dependicies

	sudo apt-get install python-virtualenv

Clone m00se to start working on him

	git clone git@github.com:ZachOrr/m00se.git
	cd m00se

Set up a virtualenv and install all the necessary dependicies

	virtualenv -p `which python2` venv
	source venv/bin/activate
	pip install -r requirements.txt

If you want to test the Gist feature locally, make sure you have a token from Github in a file named `github_oauth_token`

	echo MY_TOKEN_HERE > github_oauth_token

## To Do

* Itegrate with Google Calendar to update topic
* Gists for the same problem name should make a revision
* Allow indexing by numbers and names
* Put arguments needed in the dictionary so 1) the help can be printed out better and 2) adding new endpoints is super easy
* !leet to give someone a 1337 h4ckz0r point so we can synergize our gamification buzzword buzzword
* !seen to check which problem someone was last seen working on. Maybe do the same thing to see who has contribuited to a problem so far, and mention all contribuitors without needed to look at a gist
* Make Github token optional, so people just testing out a feature don't need to have a file for it
* Write some unit tests to test features
* Write a fake irc server that the bot can connect to so people can try out commands they're implementing without needing to hook it up to an irc server
* Write in a hash identification function !id [hash]
