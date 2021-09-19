import django
from django.db import models
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser, update_last_login
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    follower_count = models.IntegerField(default=0)
    profile_last_updated = models.DateTimeField(default=django.utils.timezone.now)
    avatar_url = models.URLField(default="https://avatars.githubusercontent.com/u/74496363?v=4")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        username = instance.username
        link = 'https://api.github.com/users/'+username
        date = datetime.now()
        try:
            response = requests.get(link)
            response.encoding = 'utf8'
            follower_count = response.json()['followers']
            avatar_url = response.json()['avatar_url']
        except:
            follower_count = 0
            avatar_url = "https://avatars.githubusercontent.com/u/74496363?v=4"
        Profile.objects.create(user=instance, follower_count = follower_count, profile_last_updated = date, avatar_url = avatar_url)

class Repository(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField(default=0)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    owner_username = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=Profile, dispatch_uid = "Create Repositories")
def create_repos(sender, instance, **kwargs):
    username = instance.user.username
    link = 'https://api.github.com/users/'+username+'/repos'
    try:
        response = requests.get(link)
        response.encoding = 'utf8'
        repos = []
        for i in response.json():
            repos.append([i['stargazers_count'], i['name'], i['description']])
        repos.sort(reverse=True)
        repo_names = []
        stars = []
        descriptions = []
        repo_names = list(map(lambda x:x[1], repos))
        stars = list(map(lambda x:x[0], repos))
        descriptions = list(map(lambda x:x[2], repos))
        for i in range(len(stars)):
            if descriptions[i] is None:
                descriptions[i] = ""
        for i in range(len(repos)):
            Repository.objects.create(name = repo_names[i], stars = stars[i], owner = instance, owner_username = instance.user.username, description = descriptions[i])
    except:
        pass