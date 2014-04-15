Crowdshop Server [![Codeship Status for leeonlee/crowdshop-serv](https://www.codeship.io/projects/665e9fe0-9e9b-0131-49c8-6626d4860316/status?branch=master)](https://www.codeship.io/projects/18062)
================

Below are the API calls available and the keys they return

/users/  
returns list of all users  

	id
	username
	first_name
	last_name

/users/id/  
returns information of user with id of id

	id
	username
	first_name
	last_name
	list of all tasks owned by user (see /tasks/id/ for format)

/tasks/  
returns all tasks

	owner (username of user who owns the task)
	title
	id of task
	desc
	reward
	timeStamp
	claimed_by

Filters available
- username
- exclude_user
- claimed
- claimed_by

/tasks/id/
return information of task with id of id

	owner (username of user who owns the task)
	title
	id of task
	desc
	reward
	timeStamp
	claimed_by

TODO
====
- delete password field

