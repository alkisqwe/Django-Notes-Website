from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import datetime

class Note(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    moded = models.IntegerField(default=0)
    notename = models.CharField(max_length=100,default="unamed")
    permission = models.IntegerField()
    note = models.TextField()
    notedate = models.DateTimeField(default=datetime.datetime.now())
