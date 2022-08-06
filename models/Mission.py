from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
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
	created_by = models.ForeignKey(
		User, 
		related_name='mission_created_by', 
		null=True,
		blank=True,
		on_delete=models.SET_NULL
	)
	date_created = models.DateTimeField(
		auto_now_add=True, 
		null=True
	)
	date_modified = models.DateTimeField(auto_now=True)
	modified_by = models.ForeignKey(
		User, 
		on_delete=models.SET_NULL, 
		null=True,
		blank=True,
		related_name = 'mission_modified_by'
	)
	comments = GenericRelation(Comment)
	discord_msg_id = models.CharField(max_length=20, 
		blank=True, 
		null=True,
		verbose_name="Discord Msg ID"
	)
	discord_api_id = models.CharField(max_length=20, 
		blank=True, 
		null=True,
		verbose_name="Discord API Event ID"
	)

	# Metadata

	class Meta:
		ordering = ["-name"]

	# Methods

	def __str__(self):
		return self.name

	def delete_discord_event(self):
		
		bot_token = WebHook.objects.get(service_name__exact='bot token').url
		api_url = WebHook.objects.get(service_name__exact='Discord Event').url
		api_headers = {
			"Authorization": bot_token,
			"Content-Type" : "application/json",
			"User-Agent" : "DiscordBot (https://your.bot/url) Python/3.9 aiohttp/3.8.1"
		}
		
		webhook_url = WebHook.objects.get(service_name__exact='Discord').url
		params = {'wait': 'true'}
		
		if self.discord_msg_id:
			
			delete_url = webhook_url + (f'/messages/{self.discord_msg_id}')
			api_delete_url = f'{api_url}/{self.discord_api_id}'
			webhook_result = requests.delete(delete_url, params = params)
			api_result = requests.delete(api_delete_url, headers = api_headers)
		
			try:
				webhook_result.raise_for_status()
			except requests.exceptions.HTTPError as err:
				print(err)
			else:
				print("Payload delivered successfully, code {}.".format(webhook_result.status_code))
				
			try:
				api_result.raise_for_status()
			except requests.exceptions.HTTPError as err:
				print(err)
			else:
				print("Payload delivered successfully, code {}.".format(api_result.status_code))
		return True
		
	def create_discord_event(self, image_url, request):
		# Create message should be
		# POST/webhooks/{webhook.id}/{webhook.token}
		
		# Edit message
		# PATCH/webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
		
		#Determine the information required for sending to webhook or API
		
		#New Discord Event API Specific Variables
		
		bot_token = WebHook.objects.get(service_name__exact='bot token').url
		api_url = WebHook.objects.get(service_name__exact='Discord Event').url
		channel_id = WebHook.objects.get(service_name__exact='channel id').url
		
		if self.mission_date and self.mission_time:
			mission_start_time = datetime.combine(self.mission_date, self.mission_time)
		else:
			mission_start_time = datetime(2030, 1, 1, 10, 0, 0)

		
		#mission_start_time = datetime.combine(self.mission_date, self.mission_time)
		mission_end_time = mission_start_time + timedelta(hours=2)
		
		#Webhook Specific Variables
		url = WebHook.objects.get(service_name__exact='Discord').url
		
		#Webhook Specific Embed Variables
		title = self.campaign.name
		mission_name = self.name
		now = str(timezone.now())
		if self.mission_date:
			date = self.mission_date.strftime("%b %d %Y")
		else:
			date = None
		description = (f'{self.name}\n**{date}, {self.mission_time} UTC**\n\n{self.description}')
		register_url = request.build_absolute_uri(reverse('mission_signup_v2', args=(self.id,)))
		mission_page = request.build_absolute_uri(reverse('mission_v2', args=(self.id,)))
		
		
		#Form the data and header json for sending.
		
		#New Discord Event API request data.
		api_data = {
			"name" : self.name,
			"description" : f'{self.description}\n**Mission Page**\n{mission_page}\n**Sign Up Sheet**\n{register_url}',
			"scheduled_start_time" : mission_start_time.isoformat(),
			"scheduled_end_time" : mission_end_time.isoformat(),
			"entity_type" : 2,
			"privacy_level" : "2",
			"channel_id" : channel_id,
		}
		api_headers = {
			"Authorization": bot_token,
			"Content-Type" : "application/json",
			"User-Agent" : "DiscordBot (https://your.bot/url) Python/3.9 aiohttp/3.8.1"
		}
		
		#Webhook Request Data
		params = {'wait': 'true'}
		data = {
			"content" : "OPTICS Generated Mission Event",
			"username" : "OPTICS Bot"
		}
		data["embeds"] = [
			{
				"title": title,
				"description": description,
				"color": 16711680,
				"fields": [
					{
						"name": "Mission Page",
						"value": (f'[{mission_name}]({mission_page})'),
						"inline": True
					},
					{
						"name": "Sign Up Sheet",
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
		
		#Check to see if a message id has been logged already. If so we are going to perform an edit.
		
		if self.discord_msg_id:
			webhook_patch_url = url + (f'/messages/{self.discord_msg_id}')
			api_patch_url = f'{api_url}/{self.discord_api_id}'
			webhook_result = requests.patch(webhook_patch_url, json = data, params = params)
			api_result = requests.patch(api_patch_url, json = api_data, headers = api_headers)
		else:
			webhook_result = requests.post(url, json = data, params = params)
			api_result = requests.post(api_url, json = api_data, headers = api_headers)
		
		# Check the response for Webhook
		
		try:
			webhook_result.raise_for_status()
			webhook_jsonResponse = webhook_result.json()
		except requests.exceptions.HTTPError as err:
			print(err)
		else:
			print("Payload delivered successfully, code {}.".format(webhook_result.status_code))
			print(webhook_jsonResponse['id'])
			self.discord_msg_id = webhook_jsonResponse['id']
			self.save()
		
		#Check the response for the API Event
		try:
			api_result.raise_for_status()
			api_jsonResponse = api_result.json()
		except requests.exceptions.HTTPError as err:
			print(err)
		else:
			print("Payload delivered successfully, code {}.".format(api_result.status_code))
			print(api_jsonResponse['id'])
			self.discord_api_id = api_jsonResponse['id']
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

