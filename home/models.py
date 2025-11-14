from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    priority_list = [
        ("low", "কম গুরুত্বপূর্ণ"),
        ("medium", "মাঝারি"),
        ("high", "গুরুত্বপূর্ণ"),
    ] 

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=260)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=priority_list, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)