from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Campaign

def campaign_add_comment(request):
	# if this is a POST request we need to process the form data
	campaign_id = request.GET.get('campaign_id')
	returnURL = request.GET.get('returnUrl')

	if request.method == 'POST':
		comment_data = request.POST.dict()
		comment = comment_data.get("comment_text")
		# Get the post object
		campaign = Campaign.objects.get(pk=campaign_id)
		campaign.comments.create(comment=comment, 
								 user=request.user)

		return HttpResponseRedirect(returnURL)