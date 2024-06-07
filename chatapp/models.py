from dataclasses import asdict

from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=1000)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='room')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    value = models.TextField()

    def __str__(self):
        return self.value
    
    
# use with related('model_name') to get the related model with 1 query ex: Room.objects.select_related('code').all()
class Code(models.Model):
    code = models.CharField(max_length=1000)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    expires = models.DateTimeField(null=True)
    
    
    def __str__(self):
        return self.code