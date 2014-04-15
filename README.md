Crowdshop Server [![Codeship Status for leeonlee/crowdshop-serv](https://www.codeship.io/projects/665e9fe0-9e9b-0131-49c8-6626d4860316/status?branch=master)](https://www.codeship.io/projects/18062)
================

Below are the API calls available and the keys they return

## /users/ ##
returns list of all users  

	id
	username
	first_name
	last_name

## /users/id/ ##
returns information of user with id of id

	id
	username
	first_name
	last_name
	list of all tasks owned by user with owner omitted(see /tasks/id/ for format)

## /tasks/ ##
returns all tasks

	owner (dict of information returned by /users/)
	title
	id (of task)
	desc
	reward
	timeStamp
	claimed_by (dict of information returned by /users/, except for claimer)

Filters available (they can be chained)
- username - Returns all tasks owned by the user with the username specified
- id - Returns all tasks owned by user with the id specified
- exclude_user - returns all tasks not owned by user specified
- exclude_id - returns all tasks not owned by id specified
- claimed - if set to false, returns all non claimed tasks; if set to true, returns all claimed tasks
- claimed_by_user - returns all tasks claimed by user with the username specified
- claimed_by_id - returns all tasks claimed by user with the id specified

## /tasks/id/ ##
return information of task with id of id

	owner (dict of information returned by /users/)
	title
	id (of task)
	desc
	reward
	timeStamp
	claimed_by (dict of information returned by /users/, except for claimer)

