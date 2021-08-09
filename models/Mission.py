from django.db import models
from django.utils import timezone
from datetime import datetime
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
# Required for Generic Keys for Comments
from django.contrib.contenttypes.fields import GenericRelation
import requests

from .Comment import *
from .WebHook import *

class Mission(models.Model):
	# Fields

	campaign = models.ForeignKey(
		"Campaign", 
		on_delete=models.CASCADE, 
		null=True
	)
	number = models.IntegerField(
		default=1,
		help_text="A number representing the mission order within the campaign.",
		verbose_name="mission number",
	)
	name = models.CharField(
		max_length=200, 
		help_text="Enter Mission Name"
	)
	description = models.TextField(
		help_text="Enter Mission Description/Situation.",
		default="Mission description to be added here.",
	)
	brief = models.TextField(
		help_text="Enter Detailed Mission Brief.",
		null=True,
		blank=True,
		verbose_name="Tactical Mission Brief",
	)
	roe = models.TextField(
		help_text="Enter Rules of Engagement",
		null=True,
		blank=True,
		verbose_name="Rules of Engagement",
	)
	munitions_restrictions = models.TextField(
		help_text="Enter any restrictions on use of munitions/weaponry.",
		null=True,
		blank=True,
		verbose_name="munitions restrictions",
	)
	mission_time = models.TimeField(
		max_length=5,
		help_text="Mission time in HH:MM format. (UTC)",
		null=True,
		blank=True,
		verbose_name="mission Start Time (UTC)",
		default="10:00",
	)
	mission_date = models.DateTimeField(
		help_text="Proposed mission Date. (UTC)",
		null=True,
		blank=True,
		verbose_name="expected Mission Date (UTC)",
	)
	notify_discord = models.BooleanField(
		default=False, 
		verbose_name="Send Notification To Discord if Webhook configured."
	)
	mission_game_time = models.CharField(
		max_length=5,
		help_text="Mission game start time in HH:MM format.",
		null=True,
		blank=True,
		verbose_name="In-Game Mission Start Time",
	)
	mission_game_date = models.DateTimeField(
		help_text="Mission game date.",
		null=True,
		blank=True,
		verbose_name="In-Game Mission Date",
	)

	# Weather
	visibility = models.CharField(
		max_length=100,
		help_text="Enter Visibility.",
		null=True,
		blank=True,
		verbose_name="Visibility",
	)
	cloud_base = models.CharField(
		max_length=10,
		help_text="Enter Cloud base in K of ft.",
		null=True,
		blank=True,
		verbose_name="Cloud Base Altitude",
	)
	cloud_top = models.CharField(
		max_length=10,
		help_text="Enter Cloud Tops in K of ft.",
		null=True,
		blank=True,
		verbose_name="Cloud Tops",
	)
	wind_sl = models.CharField(
		max_length=20,
		help_text="Enter Wind at Sea Level",
		null=True,
		blank=True,
		verbose_name="Wind at Sea Level",
	)
	wind_7k = models.CharField(
		max_length=20,
		help_text="Enter Wind at 7K ft.",
		null=True,
		blank=True,
		verbose_name="Wind at 7K ft",
	)
	wind_26k = models.CharField(
		max_length=20,
		help_text="Enter Wind at 26K ft.",
		null=True,
		blank=True,
		verbose_name="Wind at 26K ft",
	)
	qnh = models.CharField(
		max_length=20, 
		help_text="Enter QNH", 
		null=True, 
		blank=True, 
		verbose_name="QNH"
	)
	qfe = models.CharField(
		max_length=20, 
		help_text="Enter QFE", 
		null=True, 
		blank=True, 
		verbose_name="QFE"
	)
	temp = models.CharField(
		max_length=20,
		help_text="Enter temperature in C.",
		null=True,
		blank=True,
		verbose_name="Temperature in Celcius",
	)
	sigwx = models.CharField(
		max_length=20, 
		help_text="SIGWX", 
		null=True, 
		blank=True, 
		verbose_name="SIGWX"
	)
	creator = models.ForeignKey(
		User, 
		null=True, 
		blank=True, 
		on_delete=models.SET_NULL, 
		verbose_name='Mission Creator'
	)
	date_created = models.DateTimeField(
		auto_now_add=True
	)
	last_modified = models.DateTimeField(
		auto_now=True
	)
	comments = GenericRelation(Comment)
	discord_msg_id = models.CharField(max_length=20, 
		blank=True, 
		null=True,
		verbose_name="Discord Msg ID"
	)

	# Metadata

	class Meta:
		ordering = ["-name"]

	# Methods

	def __str__(self):
		return self.name

	def delete_discord_event(self):
		webhook_instance = WebHook.objects.get(service_name__exact='Discord')
		url = webhook_instance.url
		params = {'wait': 'true'}
		
		if self.discord_msg_id:
			
			delete_url = url + (f'/messages/{self.discord_msg_id}')
			result = requests.delete(delete_url, params = params)
		
			try:
				result.raise_for_status()
			except requests.exceptions.HTTPError as err:
				print(err)
			else:
				print("Payload delivered successfully, code {}.".format(result.status_code))

		return True
		
	def create_discord_event(self, image_url, request):
		# Create message should be
		# POST/webhooks/{webhook.id}/{webhook.token}
		
		# Edit message
		# PATCH/webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
		
		webhook_instance = WebHook.objects.get(service_name__exact='Discord')
		url = webhook_instance.url
		
		params = {'wait': 'true'}
		
		data = {
			"content" : "OPTICS Generated Mission Event",
			"username" : "OPTICS Bot"
		}
		title = self.campaign.name
		thumbnail = image_url
		mission_name = self.name
		now = str(timezone.now())
		date = self.mission_date.strftime("%b %d %Y")
		description = (f'{self.name}\n**{date}, {self.mission_time} UTC**\n\n{self.description}')
		register_url = request.build_absolute_uri(reverse('mission_signup', args=(self.id,)))
		mission_page = request.build_absolute_uri(reverse('mission', args=(self.id,)))
		
		print(register_url)
		
		data["embeds"] = [
			{
				"title": title,
				"description": description,
				"color": 16711680,
				"fields": [
					{
						"name": "Mission Page",
						"value": (f'[{mission_name}]({mission_page})'),
						#"value": "[Cracking Eggs With A Hammer ](http://www.google.com)",
						"inline": True
					},
					{
						"name": "Sign Up Sheet",
						#{% url 'mission_signup' self.id %}?returnUrl={{request.path}}
						"value": (f'[Register here]({register_url})'),
						"inline": True
					}
				],
				"timestamp": now,
				"thumbnail": {
					"url": image_url
				}
			}
		]
		
		
		if self.discord_msg_id:
			patch_url = url + (f'/messages/{self.discord_msg_id}')
			result = requests.patch(patch_url, json = data, params = params)
		else:
			result = requests.post(url, json = data, params = params)
		
		print(result)
		try:
			result.raise_for_status()
			jsonResponse = result.json()
		except requests.exceptions.HTTPError as err:
			print(err)
		else:
			print("Payload delivered successfully, code {}.".format(result.status_code))
			print(jsonResponse['id'])
			self.discord_msg_id = jsonResponse['id']
			self.save()
		
		return True
	
	def new(self, campaignObject):
		new_mission_instance = Mission(
			campaign = campaignObject,
			number = self.number + 1,
			name = self.name,
			description = self.description,
			brief = self.brief,
			roe = self.roe,
			munitions_restrictions = self.munitions_restrictions,
			notify_discord = False,
		)
		
		new_mission_instance.save()
		
		mission_packages = self.package_set.all()
		if mission_packages:
			for package in mission_packages:
				package.copyToMission(new_mission_instance)
		
		mission_targets = self.target_set.all()
		if mission_targets:
			for target in mission_targets:
				target.copyToMission(new_mission_instance)
		
		mission_threats = self.threat_set.all()
		if mission_threats:
			for threat in mission_threats:
				threat.copyToMission(new_mission_instance)
		
		mission_supports = self.support_set.all()
		if mission_supports:
			for support in mission_supports:
				support.copyToMission(new_mission_instance)
		
		
		#missionImagery
		
		
	def copy(self):
		campaignID = self.campaign.id
		self.new(self.campaign)
		return campaignID
		
	def copyToCampaign(self, campaign):
		campaignID = self.campaign.id
		self.new(campaign)
		return campaignID

