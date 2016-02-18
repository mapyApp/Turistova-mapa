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
    date = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input_border'}))

    class Meta:
        model = Note
        exclude = ["author","lat","lng"]

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'input_border'})
        self.fields['region'].widget.attrs.update({'class' : 'input_border'})
        self.fields['participants'].widget.attrs.update({'class' : 'input_chooser'})
        self.fields['description'].widget.attrs.update({'class' : 'input_chooser'})
        self.fields['layer'].widget.attrs.update({'class' : 'input_chooser'})
        self.fields['idea'].widget.attrs.update({'class' : 'input_chooser'})



class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'input_border'})
        self.fields['email'].widget.attrs.update({'class' : 'input_border'})
        #self.fields['password'].widget.attrs.update({'class' : 'input_border'})



class TeamForm(ModelForm):

    class Meta:
        model = Team
        exclude= ["author"]
        widgets = {
            'myfield': forms.TextInput(attrs={'class': 'input_border'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'input_border'})
        self.fields['participants'].widget.attrs.update({'class' : 'input_chooser'})
        self.fields['description'].widget.attrs.update({'class' : 'input_chooser'})

class IdeaForm(ModelForm):

    class Meta:
        model = Idea
        fields = ["name","description","team"]
        widgets = {
            'myfield': forms.TextInput(attrs={'class': 'input_border'}),
        }

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'input_border'})
        self.fields['team'].widget.attrs.update({'class' : 'input_chooser'})
        self.fields['description'].widget.attrs.update({'class' : 'input_chooser'})


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
    authorFind = forms.ModelChoiceField(User.objects.all(),required = False, label = 'Autor')

    #textFindSide = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input_border'}))



    
    
class FindFormAdvance(forms.Form):
    cursor = connection.cursor()
    dates = cursor.execute("select distinct date from mapa_note;")
    array = [("-","-")]
    for item in dates:
        st=str(item[0].day)+"."+str(item[0].month)+"."+str(item[0].year)
        array.append((st,st))
    default = array[0][0]
    Nazov =  forms.ModelMultipleChoiceField(Note.objects.all(),required = False)
    Vrstva = forms.ModelMultipleChoiceField(Layer.objects.all(),required = False)
    Region = forms.ModelMultipleChoiceField(Region.objects.all(),required = False)
    Ucastnik = forms.ModelMultipleChoiceField(User.objects.all(),required = False)

    #nameFindAd = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input_border'}))

        