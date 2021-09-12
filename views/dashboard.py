from django.shortcuts import render
from django.http import HttpResponseRedirect

def mission_dashboard(request):
	context = {}
	return render(request, "v2/dashboard/mission_stats.html", context)