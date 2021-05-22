from django.db import models

class Mission(models.Model):

    # Fields

    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, null=True)
    
    number = models.IntegerField(default=1,
                                 help_text='A number representing the mission order within the campaign.',
                                 verbose_name="mission number")
    
    name = models.CharField(max_length=200,
                            help_text='Enter Mission Name')
    
    description = models.TextField(help_text='Enter Mission Description/Situation.',
                                   default="Mission description to be added here.")
    
    brief = models.TextField(help_text='Enter Detailed Mission Brief.',
                             null=True, blank=True,
                             verbose_name="Tactical Mission Brief")
    
    roe = models.TextField(help_text='Enter Rules of Engagement',
                           null=True, blank=True,
                           verbose_name="Rules of Engagement")
    
    munitions_restrictions = models.TextField(help_text='Enter any restrictions on use of munitions/weaponry.',
                                              null=True, blank=True,
                                              verbose_name="munitions restrictions")
    
    mission_time = models.CharField(max_length=5,
                                    help_text='Mission time in HH:MM format.',
                                    null=True, blank=True,
                                    verbose_name="mission Start Time")
    
    mission_date = models.DateField(help_text='Proposed mission date.',
                                    null=True, blank=True,
                                    verbose_name="expected Mission Date")
    
    mission_game_time = models.CharField(max_length=5,
                                         help_text='Mission game start time in HH:MM format.',
                                         null=True, blank=True,
                                         verbose_name="In-Game Mission Start Time")
    
    mission_game_date = models.DateField(help_text='Mission game date.',
                                         null=True, blank=True,
                                         verbose_name="In-Game Mission Date")
