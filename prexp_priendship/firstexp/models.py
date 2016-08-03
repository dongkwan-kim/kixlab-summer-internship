from django.db import models

# Create your models here.

class Politician(models.Model):
	name = models.CharField(max_length=5)
	photo = models.URLField()

