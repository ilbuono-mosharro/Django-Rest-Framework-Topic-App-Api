from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from categories.models import Category

User = get_user_model()


# Create your models here.

class Topic(models.Model):
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_topic')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_topic")
    subject = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    users_upvote = models.ManyToManyField(User, related_name="users_upvote", blank=True)
    users_downvote = models.ManyToManyField(User, related_name="users_downvote", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject)
        super(Topic, self).save(*args, **kwargs)
