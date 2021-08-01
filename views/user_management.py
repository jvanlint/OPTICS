from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

from ..decorators import unauthenticated_user, allowed_users
from django.views.decorators.csrf import csrf_protect

from ..models import UserProfile
from ..forms import NewUserForm, ProfileForm, UserForm

@unauthenticated_user
def register_request(request):
	if request.user.is_authenticated:
		return redirect("campaign")
	else:
		if request.method == "POST":
			user_form = NewUserForm(request.POST)
			if user_form.is_valid():
				user = user_form.save()
				login(request, user)
				profile_form = ProfileForm(request.POST, instance=request.user.profile)
				if profile_form.is_valid():
					profile_form.save()
					messages.success(request, "Registration successful.")
					return HttpResponseRedirect("/airops/campaign")
				else:
					messages.error(request, "Unsuccessful registration. Invalid profile information.")
					return render(
						request=request,
						template_name="dashboard/register.html",
						context={"register_form": user_form, "profile_form": profile_form},
					)
			else:
				messages.error(request, "Unsuccessful registration. Invalid user information.")
				profile_form = ProfileForm
				return render(
					request=request,
					template_name="dashboard/register.html",
					context={"register_form": user_form, "profile_form": profile_form},
				)
		user_form = NewUserForm
		profile_form = ProfileForm
		return render(
			request=request,
			template_name="dashboard/register.html",
			context={"register_form": user_form, "profile_form": profile_form},
		)


@unauthenticated_user
@csrf_protect
def login_request(request):
	if request.user.is_authenticated:
		return redirect("campaign")
	else:
		if request.method == "POST":
			form = AuthenticationForm(request, data=request.POST)
			if form.is_valid():
				username = form.cleaned_data.get("username")
				password = form.cleaned_data.get("password")
				user = authenticate(username=username, password=password)
				if user is not None:
					login(request, user)
					messages.info(request, "You are now logged in as " + username + ".")
					return redirect("campaign")
				else:
					messages.error(request, "Invalid username or password.")
			else:
				messages.error(request, "Invalid username or password.")
		form = AuthenticationForm()
		return render(
			request=request,
			template_name="dashboard/login.html",
			context={"login_form": form},
		)


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return HttpResponseRedirect("/airops/campaign")


def change_password(request):
	if request.method == "POST":
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, "Your password was successfully updated!")
			return redirect("change_password")
		else:
			messages.error(request, "Please correct the error below.")
	else:
		form = PasswordChangeForm(request.user)
	return render(request, "dashboard/change_password.html", {"form": form})