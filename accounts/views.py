from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile, Repository
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
import requests


class NameNecessaryForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1' ,'password2') 

# class SignUpView(generic.CreateView):
#     form_class = NameNecessaryForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'

def register(request):
    if request.method == 'POST':
        form = NameNecessaryForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            link = 'https://api.github.com/users/'+username
            try:
                response = requests.get(link)
                response.encoding = 'utf8'
                if 'message' in response.json() and response.json()['message'] == 'Not Found':
                    context = {
                        'error_msg': 'No such GitHub account exists!',
                        'form': form,
                    }
                    template = loader.get_template('registration/signup.html')
                    return HttpResponse(template.render(context, request))
            except:
                context = {
                    'error_msg': 'Response not available!',
                    'form': form,
                }
                template = loader.get_template('registration/signup.html')
                return HttpResponse(template.render(context, request))
            form.save()
            return redirect('/explore')
        else:
            context = {
                'error_msg': 'Invalid form!',
                'form': form,
            }
            template = loader.get_template('registration/signup.html')
            return HttpResponse(template.render(context, request))
    else:
        form = NameNecessaryForm
        template = loader.get_template('registration/signup.html')
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))