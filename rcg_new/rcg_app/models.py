from django.db import models
import datetime as datetime

class Gender(models.Model):
	artist = models.CharField(max_length=200)
	gender = models.CharField(max_length=2)

	def __str__(self):
		return self.artist

class Groups(models.Model):
	group_name = models.CharField(max_length=200)
	members = models.CharField(max_length=200)

	def __str__(self):
		return self.group_name

class Weekly_Count(models.Model):
	week = models.CharField(max_length=50, default=datetime.datetime.today().strftime('%m-%d-%Y'))
	date_created = models.DateField(auto_now_add=True)
	M = models.IntegerField(default=0)
	F = models.IntegerField(default=0)
	X = models.IntegerField(default=0)

	def __str__(self):
		return self.week