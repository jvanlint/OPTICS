from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from .Comment import *


class Campaign(models.Model):
    # Fields

    name = models.CharField(
        max_length=200, 
        help_text="The Campaign Name.",
        verbose_name='Campaign Name'
    )
    description = models.TextField(
        help_text="A brief description used for display purposes on selection screens.",
        default="Campaign description to be added here.",
        verbose_name='Campaign Description'
    )
    dcs_map = models.ForeignKey(
        "Terrain", 
        on_delete=models.CASCADE, 
        null=True, 
        verbose_name="DCS Map"
    )
    start_date = models.DateField(
        help_text="Proposed Start Date of Campaign.",
        blank=True,
        null=True,
        verbose_name="Expected Start Date",
    )
    campaignImage = ResizedImageField(
        verbose_name="Campaign Image Thumbnail.",
        size=[500, 300],
        upload_to="campaign/thumbnails/",
        help_text="Campaign Image File.",
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        "Status", 
        on_delete=models.CASCADE, 
        null=True
    )
    situation = models.TextField(
        help_text="A detailed overview of the background and situation for the campaign.",
        null=True,
        blank=True,
    )
    aoImage = ResizedImageField(
        verbose_name="area of Operations Image",
        size=[1500, 1200],
        upload_to="campaign/ao_images",
        help_text="An image of the Area of Operations.",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User, 
        related_name='campaign_created_by', 
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
        related_name = 'campaign_modified_by'
    )
    
    comments = GenericRelation(Comment)

    # Metadata

    class Meta:
        ordering = ["-name"]

    # Methods

    def __str__(self):
        return self.name
