from django.contrib import admin
from profiles_api import models
# Register your models here.

admin.site.register(models.UserProfile) #register the UserProfile model with the admin site to manage user profiles via admin interface
admin.site.register(models.ProfileFeedItem) #register the ProfileFeedItem model with the admin site to manage profile feed items via admin interface
