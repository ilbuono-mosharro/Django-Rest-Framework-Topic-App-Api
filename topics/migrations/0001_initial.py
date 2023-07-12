# Generated by Django 4.2.3 on 2023-07-12 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=250)),
                ('body', models.TextField()),
                ('upvote', models.IntegerField(default=0)),
                ('downvote', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_topic', to='categories.category')),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_topic', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]