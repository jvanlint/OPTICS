import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

from ..models import Package, Mission, PackageImagery, UserProfile, Comment
from ..forms import PackageForm, PackageImageryForm

@login_required(login_url="account_login")
def package_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	flights = package.flight_set.all()
	comments = package.comments.all()
	user_profile = UserProfile.objects.get(user=request.user)
	imagery = package.packageimagery_set.all()
	
	breadcrumbs = {'Home': reverse('campaigns'),  package.mission.campaign.name: reverse('campaign_detail_v2', args=(package.mission.campaign.id,)), package.mission.name: reverse('mission_v2', args=(package.mission.id,)), package.name:''}
 
	context = {
			   'package_object': package,
			   'flight_object': flights,
			   "imagery_object": imagery,
			   "comments": comments,
			   "isAdmin": user_profile.is_admin(),
			   'breadcrumbs': breadcrumbs,
			   }

	return render(request, 
				  'v2/package/package.html', 
				  context=context)

@login_required(login_url="account_login")
def package_add_v2(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')

	form_title = 'Package'

	form = PackageForm(initial={'mission': mission})

	if request.method == "POST":
		form = PackageForm(request.POST, request.FILES)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.modified_by = request.user
			obj.created_by = request.user
			obj.save()
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def package_update_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Package'

	form = PackageForm(instance=package)

	if request.method == "POST":
		form = PackageForm(request.POST, instance=package)
		print(request.path)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.modified_by = request.user
			obj.save()
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)
	
@login_required(login_url="account_login")
def package_delete_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	package.delete()
	
	return HttpResponseRedirect(returnURL)
	
# ---------------- Package Comments -------------------------

@login_required(login_url="account_login")
def package_add_comment(request):
	# if this is a POST request we need to process the form data
	package_id = request.GET.get("package_id")

	if request.method == "POST":
		comment_data = request.POST.dict()
		comment = comment_data.get("comment_text")
		# Get the post object
		package_object = Package.objects.get(pk=package_id)
		package_object.comments.create(comment=comment, user=request.user)
		comments = package_object.comments.all()

	context = {
		"comments": comments,
		"package_object": package_object,
	}
	
	return render(request, "v2/package/includes/comments.html", context=context)

@login_required(login_url="account_login")
def package_delete_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	
	comment.delete()
	
	package_id = request.GET.get('package_id')
	package = Package.objects.get(id=package_id)
	comments = package.comments.all()
	
	context = {
		"comments": comments,
		"package_object": package,
	}
	
	return render(request, "v2/package/includes/comments.html", context=context)
	
def package_edit_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	
	package_id = request.GET.get('package_id')
	package = Package.objects.get(id=package_id)
	
	context = {
		"comment": comment,
		"package_object": package,
	}
	
	return render(request, "v2/package/includes/comment_edit.html", context=context)

def package_show_comments(request):
	
	package_id = request.GET.get('package_id')
	package = Package.objects.get(id=package_id)
	comments = package.comments.all()
	
	context = {
		"comments": comments,
		"package_object": package,
	}
	
	return render(request, "v2/package/includes/comments.html", context=context)

def package_update_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	package_id = request.GET.get('package_id')
	
	if request.method == 'POST':
		comment_data = request.POST.dict()
		comment_text = comment_data.get("comment_edit_text")
		comment.comment = comment_text
		comment.save()
	
	package = Package.objects.get(id=package_id)
	comments = package.comments.all()
	
	context = {
		"comments": comments,
		"package_object": package,
	}
	
	return render(request, "v2/package/includes/comments.html", context=context)
	
# ---------------- Package Imagery -------------------------
	
@login_required(login_url="account_login")
def package_imagery_create_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")

	form = PackageImageryForm(initial={"package": package})
	form_title = "Package Image"

	if request.method == "POST":
		form = PackageImageryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {
		"form": form,
		"form_title": form_title,
		"link": link_id,
		"returnURL": returnURL,
	}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def package_imagery_update_v2(request, link_id):
	imagery = PackageImagery.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")

	form_title = "Package Image"
	form = PackageImageryForm(instance=imagery)

	if request.method == "POST":
		form = PackageImageryForm(request.POST, request.FILES, instance=imagery)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {
		"form": form,
		"form_title": form_title,
		"link": link_id,
		"returnURL": returnURL,
	}
	return render(request, 'v2/generic/data_entry_form.html', context=context)


@login_required(login_url="account_login")
def package_imagery_delete_v2(request, link_id):
	imagery = PackageImagery.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	
	# Check to see if an AO Image exists.
	if imagery:
		os.remove(os.path.join(settings.MEDIA_ROOT, str(imagery.image)))
		
	imagery.delete()
	return HttpResponseRedirect(returnURL)