from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MemberModel(models.Model):
    room=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class TweetModel(models.Model):
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    good=models.IntegerField(null=True, blank=True, default=0)

class GoodModel(models.Model):
    good_by=models.ForeignKey(User,on_delete=models.CASCADE)
    content_id=models.ForeignKey(TweetModel,on_delete=models.CASCADE)