from django.contrib import admin
from .models import*
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Note)
admin.site.register(Region)
admin.site.register(Layer)
admin.site.register(Team)
admin.site.register(Idea)
admin.site.register(Comment)
