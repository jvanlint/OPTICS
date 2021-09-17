from django.shortcuts import render
from django.http import HttpResponseRedirect

def about(request):
	context = {}
	return render(request, "v2/about/about.html", context)