from __future__ import unicode_literals

from django.db import models


class User(models.Model):
	username = models.CharField(max_length=20,default='')
	password = models.CharField(max_length=20,default='')
	email = models.EmailField(default='')
	activation_key = models.IntegerField(default=1234)
	activation_status = models.IntegerField(default=0)

