from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

#User profile model to store extra user data along with default django user model
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='userprofile')
    avatar = models.ImageField(upload_to="avatar-photos", blank=True)
    age = models.IntegerField(null=True, blank= True)
    bio = models.URLField(max_length=420, null=True, blank=True)
    friends = models.ManyToManyField("UserProfile", blank= True)
    confirmed = models.BooleanField(default=False,blank= True)
    token = models.CharField(max_length=420, null=True,blank= True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

#Post model 
class Post(models.Model):
    desc = models.CharField(max_length=42, null=False,blank=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    attachment = models.ImageField(upload_to="attachment-photos",null=True,blank=True)
    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    comments = models.ManyToManyField("Comment", related_name='post', blank=True)
    def __str__(self):
        return self.desc

#Comment model 
class Comment(models.Model):
    desc = models.CharField(max_length=42, null=False,blank=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self):
        return self.desc
