# Generated by Django 3.2.7 on 2021-09-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210909_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follower_count',
            field=models.IntegerField(default=0),
        ),
    ]
