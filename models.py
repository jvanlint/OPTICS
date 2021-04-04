from django.db import models
from django_resized import ResizedImageField

# Create your models here.


class Campaign(models.Model):

    # Fields
    name = models.CharField(
        max_length=200, help_text='The Campaign Name.')
    description = models.TextField(
        help_text='A brief description used for display purposes on selection screens.', default="Campaign description to be added here.")
    dcs_map = models.ForeignKey(
        'Terrain', on_delete=models.CASCADE, null=True, verbose_name="dcs Terrain")
    start_date = models.DateField(
        help_text='Proposed Start Date of Campaign.', blank=True, null=True, verbose_name="Expected Start Date")
    campaignImage = ResizedImageField(verbose_name='Campaign Image File.', size=[500, 300],
                                      upload_to='campaign/thumbnails/', help_text='Campaign Image File.', null=True, blank=True)
    status = models.ForeignKey(
        'Status', on_delete=models.CASCADE, null=True)
    created_by = models.CharField(
        max_length=200, help_text='Name of campaign creator.', null=True, blank=True)
    situation = models.TextField(
        help_text='A detailed overview of the background and situation for the campaign.', null=True, blank=True)
    aoImage = models.ImageField(
        upload_to='campaign/ao_images/', null=True, blank=True, help_text='An image of the Area of Operations.', verbose_name="area of Operations Image")

    # Metadata

    class Meta:
        ordering = ['-name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name


class Terrain(models.Model):
    name = models.CharField(
        max_length=20, help_text='Enter Terrain Map Name.')

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name


class Status(models.Model):
    name = models.CharField(
        max_length=20, help_text='Enter Status Type')

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name


class Mission(models.Model):
    campaign = models.ForeignKey(
        'Campaign', on_delete=models.CASCADE, null=True)
    number = models.IntegerField(
        default=1, help_text='A number representing the mission order within the campaign.', verbose_name="mission number")
    name = models.CharField(
        max_length=200, help_text='Enter Mission Name')
    description = models.TextField(
        help_text='Enter Mission Description/Situation.', default="Mission description to be added here.")
    brief = models.TextField(
        help_text='Enter Detailed Mission Brief.', null=True, blank=True, verbose_name="Tactical Mission Brief")
    roe = models.TextField(
        help_text='Enter Rules of Engagement', null=True, blank=True, verbose_name="Rules of Engagement")
    munitions_restrictions = models.TextField(
        help_text='Enter any restrictions on use of munitions/weaponry.', null=True, blank=True, verbose_name="munitions restrictions")
    mission_time = models.CharField(
        max_length=5, help_text='Mission time in HH:MM format.', null=True, blank=True, verbose_name="mission Start Time")
    mission_date = models.DateField(
        help_text='Proposed mission date.', null=True, blank=True, verbose_name="expected Mission Date")

    # Metadata

    class Meta:
        ordering = ['-name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class Package(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter Package Name')
    description = models.TextField(
        help_text='Enter Mission Description/Situation.', null=True, blank=True)
    mission = models.ForeignKey(
        'Mission', on_delete=models.CASCADE, null=True)

    # Metadata
    class Meta:
        ordering = ['-name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class Flight(models.Model):
    callsign = models.CharField(
        max_length=200, help_text='Enter Flight Callsign')
    radio_frequency = models.CharField(
        max_length=20, help_text='Enter Flight Frequency', blank=True, null=True)
    tacan = models.CharField(
        max_length=5, help_text='Enter Flight TACAN (if applicable)', blank=True, null=True)
    package = models.ForeignKey(
        'Package', on_delete=models.CASCADE, null=True)

    # Metadata
    class Meta:
        ordering = ['callsign']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.callsign


class Aircraft(models.Model):
    type = models.ForeignKey(
        'Airframe', on_delete=models.CASCADE, null=True)
    flight = models.ForeignKey(
        'Flight', on_delete=models.CASCADE, null=True)

    # Metadata
    class Meta:
        ordering = ['type']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])


class Airframe(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter Airframe Name')
    stations = models.IntegerField(default=2)

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
