# Generated by Django 3.2.7 on 2021-09-18 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_profile_avatar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
