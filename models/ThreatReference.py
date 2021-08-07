from django.db import models
from django_resized import ResizedImageField

class ThreatReference(models.Model):
	# Fields

	GROUND_THREAT_CLASS = (
		("AAA", "AAA"),
		("MANPAD", "MANPAD"),
		("SHORAD", "SHORAD"),
		("MEDRAD", "MEDRAD"),
		("LONRAD", "LONRAD"),
		("TGTRDR", "TGTRDR"),
		("EWR-ACQR", "EWR-ACQR"),
	)

	GROUND_THREAT_TYPE = (
		("OPTICAL", "OPTICAL"),
		("RADAR", "RADAR"),
		("LASER", "LASER"),
		("IR", "IR"),
	)

	name = models.CharField(max_length=60)
	nato_code = models.CharField(max_length=60)
	threat_class = models.CharField(
		max_length=10, choices=GROUND_THREAT_CLASS, null=True
	)
	threat_type = models.CharField(max_length=10, choices=GROUND_THREAT_TYPE, null=True)

	gun_ammo = models.IntegerField(default=0, help_text="Number of gun rounds.")
	missile_ammo = models.IntegerField(default=0, help_text="Number of missiles.")
	range_min = models.DecimalField(
		default=0,
		help_text="Minimum engagement range (nmi).",
		decimal_places=2,
		max_digits=8,
	)
	range_max = models.DecimalField(
		default=0,
		help_text="Maximum enagengagementement range (nmi).",
		decimal_places=2,
		max_digits=8,
	)
	alt_min = models.DecimalField(
		default=0,
		help_text="Minimum engagement altitude (ft).",
		decimal_places=2,
		max_digits=8,
	)
	alt_max = models.DecimalField(
		default=0,
		help_text="Maximum engagement altitude (ft).",
		decimal_places=2,
		max_digits=8,
	)
	acquire_time = models.DecimalField(
		default=0, help_text="Time to acquire (secs).", decimal_places=2, max_digits=8
	)

	rwr_image = ResizedImageField(
		verbose_name="RWR Identifier",
		upload_to="threats",
		help_text="Upload image for rwr.",
		null=True,
		blank=True,
	)
	rwr_image2 = ResizedImageField(
		verbose_name="RWR Identifier",
		upload_to="threats",
		help_text="Upload image for rwr.",
		null=True,
		blank=True,
	)
	rwr_image3 = ResizedImageField(
		verbose_name="RWR Identifier",
		upload_to="threats",
		help_text="Upload image for rwr.",
		null=True,
		blank=True,
	)

	harm_code = models.CharField(max_length=25, null=True)

	class Meta:
		ordering = ["name"]
		verbose_name = "Threat Reference"
		verbose_name_plural = "Threat References"

	# Methods

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of MyModelName."""
		return reverse("model-detail-view", args=[str(self.id)])

	def __str__(self):
		"""String for representing the MyModelName object (in Admin site etc.)."""
		return self.name + " / " + self.nato_code