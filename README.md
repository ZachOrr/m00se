# m00se

ECX Inc's IRC bot - used to save information (links, snippets, etc) on challenges we're working on so others can view them. Maybe we'll make it do some more cool things

## Seting Up

You'll need some dependencies. First, make sure you have virtualenv installed so we can sandbox dependencies

	sudo apt-get install python-virtualenv

Clone m00se to start working on him

	git clone git@github.com:ZachOrr/m00se.git
	cd m00se

Set up a virtualenv and install all the necessary dependencies

	virtualenv -p `which python2` venv
	source venv/bin/activate
	pip install -r requirements.txt

If you want to test the Gist feature locally, make sure you have a token from Github in a file named `github_oauth_token`

	echo MY_TOKEN_HERE > github_oauth_token

For now, you'll have to comment out the Redis and Github bits if you're not going to make use of them.

## Adding a new method

To add a new method, add another entry in the commands dictionary. The entries should look like this

	"method_name": {
		"number_of_args": 1,
		"username": True,
		"text": "!method_name [the first arg] - Some info about what this does",
		"method": self.method_name,
	},

`handle_message` will pass you the number of arguments you specify with `number_of_args`. If `number_of_args` is set to -1, you get passed a list of what the user passed in (split on spaces). If `username` is True, the first argument passed to your function will be a username of the user that called that function. The `text` section should be some helpful text about how your function works. `method` should be the method you define later on. An example method for this function would look like

	def method_name(self, username, first_arg):
		# do something
		self.send_message("I did that thing!")

## To Do

* Itegrate with Google Calendar to update topic
* Gists for the same problem name should make a revision
* !leet to give someone a 1337 h4ckz0r point so we can synergize our gamification buzzword buzzword
* !seen to check which problem someone was last seen working on. Maybe do the same thing to see who has contribuited to a problem so far, and mention all contribuitors without needed to look at a gist
* Write some unit tests to test features
* Make redis/Github dependencies optional, but disable features
