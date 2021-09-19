from accounts.models import Profile, Repository
import django
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
import requests

def profile_user(request, username):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    template = loader.get_template('profile.html')
    user_here = User.objects.get(username=username)
    profile_here = Profile.objects.get(user=user_here)
    context = {
        'url_username': username,
        'full_name': user_here.get_full_name(),
        'follow': profile_here.follower_count,
        'repos': profile_here.repository_set.all(),
        'time': profile_here.profile_last_updated,
        'avatar_url': profile_here.avatar_url,
    }
    return HttpResponse(template.render(context, request))

def update(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    username = request.user.username
    link = 'https://api.github.com/users/'+username
    try:
        response = requests.get(link)
        response.encoding = 'utf8'
        followers = response.json()['followers']
        avatar_url = response.json()['avatar_url']
        Profile.objects.filter(user=request.user).update(follower_count=followers, profile_last_updated=django.utils.timezone.now(), avatar_url=avatar_url)
    except:
        return redirect(f'/profile/{username}')
    thisUser = Profile.objects.filter(user=request.user)[0]
    link = 'https://api.github.com/users/'+username+'/repos'
    try:
        response = requests.get(link)
        Repository.objects.filter(owner=thisUser).delete()
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
            Repository.objects.create(name = repo_names[i], stars = stars[i], owner = thisUser, owner_username = username, description = descriptions[i])
    except:
        pass
    return redirect(f'/profile/{username}')

def user_list(request):
    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        profile_list = Profile.objects.all()
        context = {
            'profiles': profile_list,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/accounts/login')