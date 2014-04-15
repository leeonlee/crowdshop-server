Crowdshop Server [![Codeship Status for leeonlee/crowdshop-serv](https://www.codeship.io/projects/665e9fe0-9e9b-0131-49c8-6626d4860316/status?branch=master)](https://www.codeship.io/projects/18062)
================

/users/

returns list of all users

	id
	username
	first name
	last name

/users/id

returns information of user with id of id

	id
	username
	first name
	last name
	list of all tasks owned by user (see /tasks/id for format)

/tasks/

returns all tasks

	- owner (username of user who owns the task)
	- title
	- id of task
	- desc
	- reward
	- timeStamp
	- claimed_by

/users/
- all users

/opentasks/user/
- tasks open to user

/requestedtasks/user/
- tasks made by user

/claimedtasks/user/
- tasks taken on by user

TODO
====
- delete password field

