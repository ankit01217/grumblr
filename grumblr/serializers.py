from __future__ import unicode_literals
from grumblr.models import *
from django.contrib.auth.models import User
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
	    model = User
	    fields = ('username', 'first_name', 'last_name', 'email', 'id')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
	    model = UserProfile
	    fields = ('avatar', 'age', 'bio','user', 'id')

class CommentSerializer(serializers.ModelSerializer):
	userprofile = UserProfileSerializer()
	class Meta:
	    model = Post
	    fields = ('desc', 'timestamp', 'userprofile', 'id')

class PostSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True)
	userprofile = UserProfileSerializer()
	class Meta:
	    model = Post
	    fields = ('id', 'desc', 'timestamp', 'attachment', 'userprofile', 'comments')

