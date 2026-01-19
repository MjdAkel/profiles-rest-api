from django.db import models
from django.contrib.auth.models import AbstractUser #to customize user model for authentication
from django.contrib.auth.models import PermissionsMixin #to add permission features to the user model
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
#to create custom manager for user profile model

# Create your models here.

class UserProfileManager(BaseUserManager):

    def create_user(self, email, name ,username, password=None): #create and return a normal user
        """Create and return a normal user"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email) #normalize the email address by lowercasing the domain part
        user = self.model(email=email, name=name,username=username) #create a new user instance with the normalized email and provided name
        user.set_password(password) #set the user's password using set_password method to hash the password
        user.save(using=self._db) #save the user to the database

        return user

    def create_superuser(self, email, name, password): #create and return a superuser
        """Create and return a superuser"""
        user = self.create_user(email, name, password) #create a normal user first

        user.is_superuser = True #set is_superuser to true for superuser
        user.is_staff = True # set is_staff to true for superuser

        user.save(using=self._db) #save the superuser to the database
        return user  #return the created superuser


class UserProfile(AbstractUser,PermissionsMixin): #class for user profile parameter is AbstractUser to customize user model and PermissionsMixin to add permission features
    """Data base model for users in the system """
    email = models.EmailField(max_length=50, unique=True) #email field with max length 50 and unique constraint
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff =models.BooleanField(default=False) #to determine if user is staff or not
    username = models.CharField(max_length=255, unique=True) 
    objects =UserProfileManager() #custom manager for user profile model for creating users and superusers
    USERNAME_FIELD ='email' #specifies that email field will be used for authentication instead of username
    REQUIRED_FIELDS = ['name', 'username'] #specifies that name field is required when creating a user via createsuperuser command

    
    def get_full_name(self): #method to get full name of user
        return self.name #return name as full name

    def get_short_name(self): #method to get short name of user
        return self.name #return name as short name
    
    def __str__(self): #string representation of user object
        return self.email #return email as string representation of user object
    
# a model is a class in django that represents a database table
# and defines the structure of the table and the data it will store. 


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, #linking the feed item to a specific user profile using foreign key relationship
        on_delete=models.CASCADE #if the user profile is deleted, all associated feed items will also be deleted
    )
    status_text = models.CharField(max_length=255) #text field to store the status update with max length 255
    created_on = models.DateTimeField(auto_now_add=True) #timestamp field to store the creation time of the feed item, automatically set when created

    def __str__(self): #string representation of feed item object
        return self.status_text #return status text as string representation of feed item objects
