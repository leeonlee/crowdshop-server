import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
	return render_to_response("crowdshop/index.html", RequestContext(request))

def login(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					results['success'] = 'success'
				else:
					results['success'] = 'validate'

	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')