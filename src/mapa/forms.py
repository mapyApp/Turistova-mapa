#!/usr/bin/env python
from django.forms import ModelForm
from django import forms
from models import*
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.db import connection

class NoteForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    class Meta:
        model = Note
        exclude = ["lat","lng"]
    
class UserProfilForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar"]
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 128
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email"]
        
class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
        
class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ["name","description"]

class FindForm(forms.Form):
    cursor = connection.cursor()
    dates = cursor.execute("select distinct date from mapa_note;")
    array = [("-","-")]
    for item in dates:
        st=str(item[0].day)+"."+str(item[0].month)+"."+str(item[0].year)
        array.append((st,st))
    default = array[0][0]
    name =  forms.ModelChoiceField(Note.objects.all(),required = False)
    layer = forms.ModelChoiceField(Layer.objects.all(),required = False)
    date = forms.ChoiceField(choices=array,required = False)
    region = forms.ModelChoiceField(Region.objects.all(),required = False)
    user = forms.ModelChoiceField(User.objects.all(),required = False)
    

        