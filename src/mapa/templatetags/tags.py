from django import template
from ..models import *
from ..forms import FindForm
from itertools import chain
from django.http import Http404
register = template.Library()


def value(st):
    if st!= "":
        return st
    return-1

def dateFormat(post):
    if post != ("-"):
        date = post.split(".")
        return date[2]+"-"+date[1]+"-"+date[0]
    return "2000-2-2"

@register.inclusion_tag('showMapTemplate.html',takes_context=True)
def show_map(context):
    
    request = context['request']
    if "find" in request.POST:
        notesLayer= Note.objects.filter(layer__id=value(request.POST["layerFind"]))
        notesName = Note.objects.filter(id=value(request.POST["nameFind"]))
        notesRegion = Note.objects.filter(region=value(request.POST["regionFind"]))
        notesUser = Note.objects.filter(participants__id=value(request.POST["userFind"]))
        notesDate = Note.objects.filter(date=dateFormat(request.POST["dateFind"]))
        notesAuthor =  Note.objects.filter(author__id=value(request.POST["authorFind"]))
        notes = list(chain(notesLayer,notesName,notesRegion,notesUser,notesDate,notesAuthor))
        
        findForm = FindForm()
        
        
        if request.POST["layerFind"]:
            l = Layer.objects.get(id=request.POST["layerFind"])
        else:    
            l = Layer.objects.get(id=1)
        return  dict(layer=l,notes=notes,findForm = findForm)
    try:
        l = Layer.objects.get(id=1)
    except Layer.DoesNotExist:
        raise Http404("Vrstva neexistuje!!")
    notes = Note.objects.filter(layer=l)
    findForm = FindForm()    
    return dict(layer=l,notes=notes,findForm = findForm)

    notes=set()
    if "advanceFind" in request.POST:
        query = request.POST.getlist("layerFindAd")
        for item in query:
            map(notes.add,Note.objects.filter(layer__id=value(item)))
        query = request.POST.getlist("nameFindAd")
        for item in query:
            map(notes.add,Note.objects.filter(id=value(item)))
        query = request.POST.getlist("regionFindAd")
        for item in query:
            map(notes.add,Note.objects.filter(region=value(item)))
        query = request.POST.getlist("userFindAd")
        for item in query:
            map(notes.add,Note.objects.filter(participants__id=value(item)))

@register.inclusion_tag('searchingMap.html')
def searching():
    findForm = FindForm() 
    return {'findForm': findForm}

@register.inclusion_tag('listNotesTemplate.html')
def listNotes(user):
    notes = Note.objects.filter(participants__id=user.id).order_by("-id")
    return dict(notes=notes)
    


