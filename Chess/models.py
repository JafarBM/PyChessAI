from __future__ import unicode_literals
from django.db import models


class User(models.Model):
	username = models.CharField(max_length = 20,default = '')
	password = models.CharField(max_length = 20,default = '')
	email = models.EmailField(default = '')
	activation_key = models.IntegerField(default = 1234)
	activation_status = models.IntegerField(default = 0)
	user_score = models.IntegerField(default = 0)
	turn = models.BooleanField(default = True)
	white_right_rook = models.BooleanField(default = True)
	white_left_rook = models.BooleanField(default = True)
	black_right_rook = models.BooleanField(default = True)
	black_left_rook = models.BooleanField(default = True)
	black_king = models.BooleanField(default = True)
	white_king = models.BooleanField(default = True)

	user_board = models.CharField(max_length = 64 * 15, default = '')

