from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Package, PackageImagery, UserProfile
from ..forms import PackageImageryForm

@login_required(login_url="account_login")
def package_imagery_create(request, link_id):
	package = Package.objects.get(id=link_id)

	form = PackageImageryForm(initial={"package": package})

	if request.method == "POST":
		form = PackageImageryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect("/airops/package/" + str(link_id))

	context = {"form": form, "link": link_id}
	return render(request, "packageImagery/packageImagery_form.html", context=context)


@login_required(login_url="account_login")
def package_imagery_update(request, link_id):
	imagery = PackageImagery.objects.get(id=link_id)

	packageID = imagery.package.id
	form = PackageImageryForm(instance=imagery)

	if request.method == "POST":
		form = PackageImageryForm(request.POST, request.FILES, instance=imagery)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			print("Form Saved!")
			return HttpResponseRedirect("/airops/package/" + str(packageID))

	context = {"form": form, "link": packageID}
	return render(request, "packageImagery/packageImagery_form.html", context=context)


@login_required(login_url="account_login")
def package_imagery_delete(request, link_id):
	imagery = PackageImagery.objects.get(id=link_id)
	packageID = imagery.package.id
	if request.method == "POST":
		imagery.delete()
		return HttpResponseRedirect("/airops/package/" + str(packageID))

	context = {"item": imagery}
	return render(request, "packageImagery/packageImagery_delete.html", context=context)