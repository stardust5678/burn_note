from django.db import models

class SecretMessage(models.Model):
    token = models.CharField(max_length=40, unique=True, primary_key=True)
    encrypted_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()