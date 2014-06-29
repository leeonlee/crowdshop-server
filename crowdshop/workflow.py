from crowdshop.models import State

if not State.objects.all().exists():
	resolved, created = State.objects.get_or_create(name="Resolved")
	paid, created = State.objects.get_or_create(name="Paid", next_state = resolved)
	claimed, created = State.objects.get_or_create(name="Claimed", next_state = paid)
	open, created = State.objects.get_or_create(name="Open", next_state = claimed)
