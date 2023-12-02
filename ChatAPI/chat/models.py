from django.db import models
from django.conf import settings
from users.models import MyUser as User

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

class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, related_name='online_rooms', blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def is_user_online(self, user):
        return user in self.online.all()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'

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
