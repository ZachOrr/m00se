# m00se

ECX Inc's IRC bot - used to save information (links, snippets, etc) on challenges we're working on so others can view them. Maybe we'll make it do some more cool things

## Setting Up

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

## Adding a new command

To add a new command or related group of commands, create a new python source
file with an appropriate name in the `commands/` subdirectory, for example:

    commands/
        new_cmd.py
        ...

Import the `command` decorator from `decorators.py`

    from decorators import command

Then simply define your method and decorate it with options; the first
parameter passed to your command will always be the instance of `Moose`; any
other parameters passed will depend on the options you specify:

    @command("new_cmd", number_of_args=0, text="new_cmd")
    def new_cmd(moose):
        # do stuff with moose

    @command("uname_cmd", number_of_args=1, text="uname_cmd", username=True)
    def uname_cmd(moose, username, args):
        # do stuff with  moose, username, args

`handle_message` will pass you the number of arguments you specify with `number_of_args`. If `number_of_args` is set to -1, you get passed a list of what the user passed in (split on spaces). If `username` is True, the second argument passed to your function will be a username of the user that called that function. The `text` section should be some helpful text about how your function works.

## To Do

* Integrate with Google Calendar to update topic
* Write some unit tests to test features
* Make redis/Github dependencies optional, but disable features
* !leetest to show the leetest of them all
* If !get doesn't have any new data since the last !get, don't make a new gist, just serve up the old link
