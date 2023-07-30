import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_confirmation = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="images/avatars/", blank=True, validators=[
        validate_image_file_extension, FileExtensionValidator(['JPEG', 'JPG', 'PNG']),
    ])

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f'{self.username}'