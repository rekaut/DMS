# Create your views here.
from login.forms import UserForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required, user_passes_test


def register(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False

	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		# profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid...
		if user_form.is_valid() :
			# Save the user's form data to the database.
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			registered = True

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print user_form.errors
	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		# profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render_to_response(
			'login/register.html',
			{'user_form': user_form, 'registered': registered},
			context)

    # Decorator for views that checks that the user passes the given test,
    # redirecting to the log-in page if necessary. The test should be a callable
    # that takes the user object and returns True if the user passes.
# this won't allow anyone to login until user is already logged in.
@user_passes_test(lambda user: not user.username, login_url='/uploads/list/', redirect_field_name=None)
def user_login(request):
	# Like before, obtain the context for the user's request.
	context = RequestContext(request)

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				# return HttpResponseRedirect('/login/success')

				p = request.POST['username']
				# return HttpResponse('welcome '+p)
				request.session['name'] = p

				return HttpResponseRedirect('/uploads/list/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your login account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			# return HttpResponse("Invalid login details supplied.")
			return render_to_response('login/login.html', {'msg': 'Invalid username/password.'}, context)

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render_to_response('login/login.html', {}, context)

# Decorator for views that checks that the user is logged in, redirecting
#     to the log-in page if necessary.
@login_required(login_url='/login/go/')	
def success(request):
	p = request.POST['username']
	return HttpResponse('welcome '+p)

@login_required(login_url='/login/go/')	
def logout_session(request):
	logout(request)
	return HttpResponseRedirect('/')