from django.db import models
from django.conf import settings 

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] #ensures old message appear at the top, new at the bottom

    def __str__(self):
        return f'[{self.timestamp}] {self.sender.username}: {self.content}'