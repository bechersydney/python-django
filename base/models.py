from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # use 'Topic' if the model call is below the caller
    # in database when the topic is deleted it should be null
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # when using SET_NULL null=True should declared
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # make column accept null value
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']  # ascending base on created at

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # delete all message if user is deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # delete all message if room is deleted
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.body[0:50]

