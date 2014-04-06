from django.core.management.base import BaseCommand, CommandError
from crowdshop.models import *
from faker import Factory
from random import randint

fake = Factory.create()
PASSWORD = 'a'
TITLES = [
	'Whole Milk',
	'Heineken',
	'Duracell AA Batteries',
	'Lunchables Pizza',
	'Yogurt',
	'Bananas',
	'Red Bull',
	'Cookie Dough',
	'Shampoo & Conditioner',
	'Toothpaste',
]

class Command(BaseCommand):
	help = ''

	def handle(self, *args, **options):
		usernames = []
		for i in range(10):
			user = createUser()
			usernames.append(user.username)
		for i in range(len(usernames)):
			createTask(usernames[i], TITLES[i])

def createUser():
	first_name = fake.first_name()
	last_name = fake.last_name()
	email = first_name + last_name + "@gmail.com"
	username = first_name
	user = User.objects.create(username = username, first_name = first_name, 
		last_name = last_name, password = PASSWORD, email = email)
	return user

def createTask(username, title):
	username = username
	title = title
	desc = fake.text(50)
	threshold = randint(5, 20)
	reward = randint(2, 5)
	task = Task.objects.create(
				owner = User.objects.get(username = username),
				title = title,
				desc = desc, 
				threshold = threshold,
				reward = reward,
			)
	return task