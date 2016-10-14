from django.contrib import admin
from grumblr import models

from grumblr.models import UserProfile
from grumblr.models import Post

class UserProfileModelAdmin(admin.ModelAdmin):
	list_display = ["user","avatar"]
	list_display_links = ["user"]
	list_filter = ["user"]
	search_fields = ["user"]
	class Meta:
		model = UserProfile

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["userprofile","desc","timestamp"]
	list_display_links = ["timestamp"]
	list_filter = ["desc","timestamp"]
	search_fields = ["desc","timestamp"]
	list_editable = ["desc"]
	class Meta:
		model = Post

admin.site.register(Post,PostModelAdmin)
admin.site.register(UserProfile,UserProfileModelAdmin)
