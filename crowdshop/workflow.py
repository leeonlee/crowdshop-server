from crowdshop.models import State

if not State.objects.all().exists():
	resolved, created = State.objects.get_or_create(name="Resolved")
	paid, created = State.objects.get_or_create(name="Paid", next_state = resolved)
	claimed, created = State.objects.get_or_create(name="Claimed", next_state = paid)
	open, created = State.objects.get_or_create(name="Open", next_state = claimed)


from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
