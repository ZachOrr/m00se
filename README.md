# m00se

ECX Inc's IRC bot - used to save information (links, snippets, etc) on challenges we're working on so others can view them. Maybe we'll make it do some more cool things

## Seting Up

You'll need some dependicies. First, make sure you have pip and virtualenv to start working with

	sudo apt-get install python-pip
	sudo pip install virtualenv

Clone m00se to start working on him

	git clone git@github.com:ZachOrr/m00se.git
	cd m00se

Set up a virtualenv and install all the necessary dependicies

	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

## To Do

* Itegrate with Google Calendar to update topic
* Gists for the same problem name should make a revision
* Allow indexing by numbers and names
