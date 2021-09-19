from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Repository
from django.contrib.auth.models import User
from .views import NameNecessaryForm
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Repository)