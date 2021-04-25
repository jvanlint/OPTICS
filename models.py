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
    campaignImage = ResizedImageField(verbose_name='Campaign Image Thumbnail.', size=[500, 300],
                                      upload_to='campaign/thumbnails/', help_text='Campaign Image File.', null=True, blank=True)
    status = models.ForeignKey(
        'Status', on_delete=models.CASCADE, null=True)
    created_by = models.CharField(
        max_length=200, help_text='Name of campaign creator.', null=True, blank=True)
    situation = models.TextField(
        help_text='A detailed overview of the background and situation for the campaign.', null=True, blank=True)
    aoImage = models.ImageField(
        upload_to='campaign/ao_images/', null=True, blank=True, help_text='An image of the Area of Operations.', verbose_name="area of Operations Image")
    # aoImage = ResizedImageField(verbose_name='area of Operations Image', size=[1500, 1200],
    #                                  upload_to='campaign/ao_images', help_text='An image of the Area of Operations.', null=True, blank=True)

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

    # Fields

    name = models.CharField(
        max_length=20, help_text='Enter Terrain Map Name.')

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name


class Status(models.Model):

    # Fields

    name = models.CharField(
        max_length=20, help_text='Enter Status Type')

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name


class Mission(models.Model):

    # Fields

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
    mission_game_time = models.CharField(
        max_length=5, help_text='Mission game start time in HH:MM format.', null=True, blank=True, verbose_name="In-Game Mission Start Time")
    mission_game_date = models.DateField(
        help_text='Mission game date.', null=True, blank=True, verbose_name="In-Game Mission Date")

    # Weather
    visibility = models.CharField(
        max_length=100, help_text='Enter Visibility.', null=True, blank=True, verbose_name="Visibility")
    cloud_base = models.CharField(
        max_length=10, help_text='Enter Cloud base in K of ft.', null=True, blank=True, verbose_name="Cloud Base Altitude")
    cloud_top = models.CharField(
        max_length=10, help_text='Enter Cloud Tops in K of ft.', null=True, blank=True, verbose_name="Cloud Tops")
    wind_sl = models.CharField(
        max_length=20, help_text='Enter Wind at Sea Level', null=True, blank=True, verbose_name="Wind at Sea Level")
    wind_7k = models.CharField(
        max_length=20, help_text='Enter Wind at 7K ft.', null=True, blank=True, verbose_name="Wind at 7K ft")
    wind_26k = models.CharField(
        max_length=20, help_text='Enter Wind at 26K ft.', null=True, blank=True, verbose_name="Wind at 26K ft")
    qnh = models.CharField(
        max_length=20, help_text='Enter QNH', null=True, blank=True, verbose_name="QNH")
    qfe = models.CharField(
        max_length=20, help_text='Enter QFE', null=True, blank=True, verbose_name="QFE")
    temp = models.CharField(
        max_length=20, help_text='Enter temperature in C.', null=True, blank=True, verbose_name="Temperature in Celcius")
    sigwx = models.CharField(
        max_length=20, help_text='SIGWX', null=True, blank=True, verbose_name="SIGWX")

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

    # Fields

    mission = models.ForeignKey(
        'Mission', on_delete=models.CASCADE, null=True)
    name = models.CharField(
        max_length=200, help_text='Enter Package Name', verbose_name="Package Name")
    frequency = models.CharField(
        max_length=10, help_text='Enter Package Frequency', verbose_name="Package Frequency",  null=True, blank=True)
    description = models.TextField(
        help_text='Enter Mission Description/Situation.', null=True, blank=True, verbose_name="Description of package objective")

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


class Target(models.Model):

    # Fields

    mission = models.ForeignKey(
        'Mission', on_delete=models.CASCADE, null=True)
    name = models.CharField(
        max_length=50, help_text='Enter target name', verbose_name="Target Name")
    lat = models.CharField(
        max_length=200, help_text='Enter target latitude', verbose_name="Target Latitude", null=True, blank=True)
    long = models.CharField(
        max_length=200, help_text='Enter target longitude.', verbose_name="Target Longitude", null=True, blank=True)
    elev = models.CharField(
        max_length=200, help_text='Enter target elevation.', verbose_name="Target Elevation", null=True, blank=True)
    notes = models.TextField(
        help_text='Any notes relevant to the target.', null=True, blank=True, verbose_name="Notes on Target")
    target_image = models.ImageField(
        upload_to='campaign/mission/target_images/', null=True, blank=True, help_text='Upload image of the target.', verbose_name="Target Image")
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


class Flight(models.Model):

    # Fields

    package = models.ForeignKey(
        'Package', on_delete=models.CASCADE, null=True)
    callsign = models.CharField(
        max_length=200, help_text='Enter Flight Callsign')
    radio_frequency = models.CharField(
        max_length=20, help_text='Enter Flight Frequency', blank=True, null=True)
    tacan = models.CharField(
        max_length=5, help_text='Enter Flight TACAN (if applicable)', blank=True, null=True)
    targets = models.ManyToManyField(Target, blank=True)

    # Time Hacks
    timehack_start = models.CharField(max_length=10, help_text='Enter time for flight takeoff.',
                                      null=True, blank=True, verbose_name="Takeoff Time")
    timehack_rdv1 = models.CharField(
        max_length=10, help_text='Enter time for flight rendevous point 1.', null=True, blank=True, verbose_name="Time RDV 1")
    timehack_rdv2 = models.CharField(
        max_length=10, help_text='Enter time for flight rendevous point 2.', null=True, blank=True, verbose_name="Time RDV 2")
    fuel_fob = models.CharField(
        max_length=10, help_text='Fuel FOB', null=True, blank=True, verbose_name="Fuel FOB")
    fuel_joker = models.CharField(
        max_length=10, help_text='Fuel JOKER.', null=True, blank=True, verbose_name="Fuel JOKER")
    fuel_bingo = models.CharField(
        max_length=10, help_text='Fuel BINGO.', null=True, blank=True, verbose_name="Fuel BINGO")

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

    # Fields

    type = models.ForeignKey(
        'Airframe', on_delete=models.CASCADE, null=True)
    flight = models.ForeignKey(
        'Flight', on_delete=models.CASCADE, null=True)
    pilot = models.CharField(
        max_length=30, help_text='Enter Pilot Name', null=True, blank=True)
    rio_wso = models.CharField(
        max_length=30, help_text='Enter RIO/WSO Name', null=True, blank=True)
    tailcode = models.CharField(
        max_length=20, help_text='Enter A/C tail code.', null=True, blank=True)
    flight_lead = models.BooleanField(default=False)
    package_lead = models.BooleanField(default=False)

    # Metadata

    class Meta:
        ordering = ['type']

    # Methods

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])


class Airframe(models.Model):

    # Fields

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


class Threat(models.Model):

    # Fields

    mission = models.ForeignKey(
        'Mission', on_delete=models.CASCADE, null=True)

    THREAT_TYPES = (
        ('AAA', 'AAA'),
        ('SAM', 'SAM'),
        ('AIR', 'AIR'),
        ('NAVAL', 'NAVAL'),
        ('GROUND', 'GROUND'),

    )

    name = models.CharField(max_length=60)
    threat_type = models.CharField(
        max_length=10, choices=THREAT_TYPES, null=True)
    description = models.TextField(
        help_text='Enter Threat Description/Situation.', default="Threat description to be added here.")


class Support(models.Model):

    # Fields

    mission = models.ForeignKey(
        'Mission', on_delete=models.CASCADE, null=True)

    THREAT_TYPES = (
        ('AWACS', 'AWACS'),
        ('TANKER', 'TANKER'),
        ('JTAC', 'JTAC'),
        ('CARRIER', 'CARRIER'),

    )

    callsign = models.CharField(max_length=50)
    support_type = models.CharField(
        max_length=10, choices=THREAT_TYPES, null=True)
    frequency = models.CharField(max_length=10, null=True, blank=True)
    tacan = models.CharField(max_length=10, null=True, blank=True)
    altitude = models.CharField(max_length=10, null=True, blank=True)
    speed = models.CharField(max_length=10, null=True, blank=True)
    brc = models.CharField(max_length=10, null=True, blank=True)
    icls = models.CharField(max_length=10, null=True, blank=True)

    notes = models.TextField(
        help_text='Enter notes for support resource.', null=True, blank=True)


class Waypoint(models.Model):

    # Fields

    flight = models.ForeignKey(
        'Flight', on_delete=models.CASCADE, null=True)

    WAYPOINT_TYPES = (
        ('NAV', 'NAV'),
        ('IP', 'IP'),
        ('CAP', 'CAP'),
        ('STRIKE', 'STRIKE'),
        ('CAS', 'CAS'),
        ('DEAD', 'DEAD'),
        ('SEAD', 'SEAD'),
        ('BAI', 'BAI'),
        ('TAKEOFF', 'TAKEOFF'),
        ('LAND', 'LAND'),
        ('DIVERT', 'DIVERT'),
    )

    name = models.CharField(max_length=50)
    number = models.IntegerField(
        default=1, help_text='A number representing the waypoint order.', verbose_name="waypoint number")
    waypoint_type = models.CharField(
        max_length=10, choices=WAYPOINT_TYPES, null=True)
    lat = models.CharField(max_length=15, null=True, blank=True)
    long = models.CharField(max_length=15, null=True, blank=True)
    elevation = models.CharField(max_length=15, null=True, blank=True)
    tot = models.CharField(max_length=15, null=True,
                           blank=True, verbose_name="time on Target")
    notes = models.TextField(
        help_text='Enter notes for the waypoint.', null=True, blank=True)
