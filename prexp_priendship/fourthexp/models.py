from django.db import models

# Create your models here.

class Politician(models.Model):
	name = models.CharField(max_length=5)
	photo = models.URLField()
	pid = models.IntegerField()

class SubmitLog(models.Model):
	# csv
	token = models.CharField(max_length=50)
	users_fav = models.IntegerField()
	shown_list = models.CharField(max_length=100)
	select_list = models.CharField(max_length=70)
	q_kind = models.CharField(max_length=5)
