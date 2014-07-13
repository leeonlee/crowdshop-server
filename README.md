Crowdshop Server [![Codeship Status for leeonlee/crowdshop-serv](https://www.codeship.io/projects/665e9fe0-9e9b-0131-49c8-6626d4860316/status?branch=master)](https://www.codeship.io/projects/18062)
================

Below are the API calls available and their responses
All rest calls require authorization headers in the form of "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" unless stated otherwise

## /create_task ##
Allows user to create a task

	POST:
	title - title of the task (required)
	desc - extra details to describe the item(s) needed (required)
	threshold - price threshold that the person is willing to pay (required)
	reward - amount of incentive for others to complete task (required)

	Successful requests will receive HTTP_201_CREATED and no data

	Unsuccessful requests will receive HTTP_400_BAD_REQUEST along with the form errors {"errors": {"threshold": ["This field is required."], "reward": ["This field is required."], "desc": ["This field is required."], "title": ["This field is required."]}}
