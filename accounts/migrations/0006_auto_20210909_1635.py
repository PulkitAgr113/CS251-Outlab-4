# Generated by Django 3.2.7 on 2021-09-09 16:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_repository_owner_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='repos',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=None, size=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='stars',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=None, size=None),
        ),
    ]
