from django.db import models
from django.conf import settings

class Conversation(models.Model):
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="conversations_initiated"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="conversations_participated"
    )
    start_time = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='messages_sent'
    )
    text = models.CharField(max_length=200, blank=True)
    attachment = models.FileField(upload_to='message_attachments/', blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
