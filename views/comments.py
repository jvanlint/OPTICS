from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Campaign, Comment

def campaign_add_comment(request):
	# if this is a POST request we need to process the form data
	campaign_id = request.GET.get('campaign_id')
	

	if request.method == 'POST':
		comment_data = request.POST.dict()
		comment = comment_data.get("comment_text")
		# Get the post object
		campaign = Campaign.objects.get(pk=campaign_id)
		campaign.comments.create(comment=comment, 
								 user=request.user)
		comments = campaign.comments.all()
	
	context = {
		"comments": comments,
		"campaign_object": campaign,
	}
	
	return render(request, "v2/campaign/includes/comments.html", context=context)
		

def campaign_delete_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	
	comment.delete()
	
	campaign_id = request.GET.get('campaign_id')
	campaign = Campaign.objects.get(id=campaign_id)
	comments = campaign.comments.all()
	
	context = {
		"comments": comments,
		"campaign_object": campaign,
	}
	
	return render(request, "v2/campaign/includes/comments.html", context=context)
	
def campaign_edit_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	
	campaign_id = request.GET.get('campaign_id')
	campaign = Campaign.objects.get(id=campaign_id)
	
	context = {
		"comment": comment,
		"campaign_object": campaign,
	}
	
	return render(request, "v2/campaign/includes/comment_edit.html", context=context)

def campaign_show_comments(request):
	
	campaign_id = request.GET.get('campaign_id')
	campaign = Campaign.objects.get(id=campaign_id)
	comments = campaign.comments.all()
	
	context = {
		"comments": comments,
		"campaign_object": campaign,
	}
	
	return render(request, "v2/campaign/includes/comments.html", context=context)

def campaign_update_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	campaign_id = request.GET.get('campaign_id')
	
	if request.method == 'POST':
		comment_data = request.POST.dict()
		comment_text = comment_data.get("comment_edit_text")
		comment.comment = comment_text
		comment.save()

	campaign = Campaign.objects.get(pk=campaign_id)
	comments = campaign.comments.all()
	
	context = {
		"comments": comments,
		"campaign_object": campaign,
	}
	
	return render(request, "v2/campaign/includes/comments.html", context=context)
	