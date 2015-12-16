#!/usr/bin/env python
from django.forms import ModelForm
from models import*
from django.contrib.auth.models import User

class ZapisForm(ModelForm):
    class Meta:
        model = Zapis
        fields = ["nazov","datum","kraj","ucastnici","textovy_popis","vrstvy","napad"]
    



class UserProfilForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["zapis"]
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email"]
        
class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["nazov","clenovia","popis","napady"]
        
class NapadForm(ModelForm):
    class Meta:
        model = Napad
        fields = ["nazov","textovy_popis"]
    #code

        