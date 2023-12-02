from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class CustomUser(AbstractUser):
    id: models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    is_active = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)