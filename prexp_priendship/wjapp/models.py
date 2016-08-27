from django.db import models

# Create your models here.

class LWJNetwork(models.Model):
	p1 = models.CharField(max_length=5)
	p2 = models.CharField(max_length=5)
	weight = models.FloatField()
	do_i_have = models.BooleanField()

class Vote19(models.Model):
	name = models.CharField(max_length=5)
	party = models.CharField(max_length=10)
	vote = models.TextField()

class VoteVector(models.Model):
	name = models.CharField(max_length=5)
	party = models.CharField(max_length=10)
	vote = models.TextField()
