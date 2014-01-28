# m00se

ECX Inc's IRC bot - used to save information (links, snippets, etc) on challenges we're working on so others can view them. Maybe we'll make it do some more cool things

## Seting Up

You'll need some dependicies. First, make sure you have virtualenv installed so we can sandbox dependicies

	sudo apt-get install python-virtualenv

Clone m00se to start working on him

	git clone git@github.com:ZachOrr/m00se.git
	cd m00se

Set up a virtualenv and install all the necessary dependicies

	virtualenv -p `which python3` venv
	source venv/bin/activate
	pip install -r requirements.txt

## To Do

* Itegrate with Google Calendar to update topic
* Gists for the same problem name should make a revision
* Allow indexing by numbers and names
