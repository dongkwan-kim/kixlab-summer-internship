from django.db import models

# Create your models here.

class Politician(models.Model):
    name = models.CharField(max_length=5)
    photo = models.URLField()
    pid = models.IntegerField()

class SubmitLog(models.Model):
    # csv
    token = models.CharField(max_length=50)
    shown_list = models.CharField(max_length=100)
    affinity_score = models.CharField(max_length=15)
