from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from chat.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=120, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=120, blank=True, null=True, unique=True)
    password = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'CustomUser'

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        unique_together = (('sender', 'recipient'),)

    def __str__(self):
        return self.content
