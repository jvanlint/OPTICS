from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from django.db import transaction

from ..models import UserProfile
from ..forms import UserForm, ProfileForm


@login_required
@transaction.atomic
def update_profile(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, "Your profile was successfully updated!")
			return redirect("campaign")
		else:
			messages.error(request, "Please correct the error below.")
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
	return render(
		request,
		"profiles/profile.html",
		{"user_form": user_form, "profile_form": profile_form},
	)