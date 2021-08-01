import os
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import User

from ..models import Comment, UserProfile


@login_required(login_url='login')
def own_profile_view(request):
	comments = Comment.objects.filter(user=request.user)
	breadcrumbs = {'Home': reverse('campaigns'),  'Own Profile': ''}

	context = {'comments': comments, 'breadcrumbs': breadcrumbs,}
	# Render the HTML template index.html with the data in the context variable
	return render(request, 'v2/profile/profile.html', context=context)

def select_avatar(request):
	context = {}
	newfile = []
	files = os.listdir(os.path.join(
		settings.STATIC_ROOT, "assets/img/avatars/"))
	for file in files:
		newfile.append('assets/img/avatars/' + file)

	context = {'files': newfile}
	return render(request, 'v2/profile/avatar_selection.html', context=context)

def change_avatar(request):
	avatar_image = request.GET.get('avatar')
	profile = UserProfile.objects.get(user=request.user)
	profile.profile_image = avatar_image
	profile.save()

	comments = Comment.objects.filter(user=request.user)

	context = {'comments': comments}

	return render(request, 'v2/profile/profile.html', context=context)

@login_required(login_url='login')
def user_profile_view(request, link_id):
	
	user_profile = User.objects.get(pk=link_id)
	breadcrumbs = {'Home': reverse('campaigns'),  'User Profile': ''}

	comments = Comment.objects.filter(user=user_profile)

	context = {'profile_object': user_profile, 'comments': comments, 'breadcrumbs': breadcrumbs,}
	# Render the HTML template index.html with the data in the context variable
	return render(request, 'v2/profile/user_profile.html', context=context)