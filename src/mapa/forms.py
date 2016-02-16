#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        exclude = ["author","lat","lng"]
         

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username","email"]
        
class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude= ["author"]
        
class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ["name","description","team"]

class FindForm(forms.Form):
    cursor = connection.cursor()
    dates = cursor.execute("select distinct date from mapa_note;")
    array = [("-","-")]
    for item in dates:
        st=str(item[0].day)+"."+str(item[0].month)+"."+str(item[0].year)
        array.append((st,st))
    default = array[0][0]
    
    textFindSide = forms.CharField(label='Názov',max_length=50)
    layerFind = forms.ModelChoiceField(Layer.objects.all(),required = False,label = 'Vrstva')
    dateFind = forms.ChoiceField( choices=array,required = False,label = 'Dátum')
    regionFind = forms.ModelChoiceField( Region.objects.all(),required = False,label = 'Región')
    userFind = forms.ModelChoiceField(User.objects.all(),required = False,label = 'Účastník')
    authorFind = forms.ModelChoiceField(User.objects.all(),required = False, label = 'Autor',)
    
    
class FindFormAdvance(forms.Form):
    cursor = connection.cursor()
    dates = cursor.execute("select distinct date from mapa_note;")
    array = [("-","-")]
    for item in dates:
        st=str(item[0].day)+"."+str(item[0].month)+"."+str(item[0].year)
        array.append((st,st))
    default = array[0][0]
    nameFindAd =  forms.ModelMultipleChoiceField(Note.objects.all(),required = False)
    layerFindAd = forms.ModelMultipleChoiceField(Layer.objects.all(),required = False)
    regionFindAd = forms.ModelMultipleChoiceField(Region.objects.all(),required = False)
    userFindAd = forms.ModelMultipleChoiceField(User.objects.all(),required = False)
    

        