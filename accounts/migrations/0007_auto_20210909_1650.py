# Generated by Django 3.2.7 on 2021-09-09 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210909_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='repos',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='stars',
        ),
        migrations.AlterField(
            model_name='repository',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]
