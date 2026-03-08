from django.contrib.auth.models import AbstractUser
from django.db import models

#----------base user (login, permission)-----------
class User(AbstractUser):
    #act as a switches to let the system know 
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    #shared info (name, profile picture, status)
    real_name = models.CharField(max_length=255, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    status_update = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

#-----------student profile---------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"Student: {self.user.username}"

#---------------teacher profile----------------
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        
    def __str__(self):
        return f"Teacher: {self.user.username}"
    
#-------------------notification-----------------
class Notification(models.Model):
    #the user receiving the notification
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)

    #track if they have seen it yet
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"