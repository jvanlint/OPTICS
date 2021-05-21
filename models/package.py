from django.db import models


class Package(models.Model):

    # Fields

    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, null=True)
    
    name = models.CharField(max_length=200,
                            help_text='Enter Package Name',
                            verbose_name="Package Name")
    
    frequency = models.CharField(max_length=10,
                                 help_text='Enter Package Frequency',
                                 verbose_name="Package Frequency",
                                 null=True, blank=True)
    
    description = models.TextField(help_text='Enter Mission Description/Situation.',
                                   null=True, blank=True,
                                   verbose_name="Description of package objective")
