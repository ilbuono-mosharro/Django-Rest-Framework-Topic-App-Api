# Generated by Django 4.2.3 on 2023-07-30 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_myuser_email_alter_myuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
