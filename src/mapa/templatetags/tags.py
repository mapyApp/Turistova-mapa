from django import template
from ..models import *
from ..forms import FindForm
from itertools import chain
from django.http import Http404
register = template.Library()


def value(st):
    if st!= "":
        return st
    return -1

def dateFormat(post):
    if post != ("-"):
        date = post.split(".")
        return date[2]+"-"+date[1]+"-"+date[0]
    return "2000-2-2"

@register.inclusion_tag('showMapTemplate.html',takes_context=True)
def show_map(context):
    request = context['request']
    print(request.POST)
    if "find" in request.POST:
        notesLayer= Note.objects.filter(layer__id=value(request.POST["layerFind"]))
        try:
            l2 = Layer.objects.get(id=value(request.POST["layerFind"]))
            if l2.name == "all" :
                notesLayer = Note.objects.all()
        except:
            pass    
        notesName = Note.objects.filter(name__icontains=value(request.POST["textFindSide"]))
        notesRegion = Note.objects.filter(region=value(request.POST["regionFind"]))
        notesUser = Note.objects.filter(participants__id=value(request.POST["userFind"]))
        notesDate = Note.objects.filter(date=dateFormat(request.POST["dateFind"]))
        notesAuthor =  Note.objects.filter(author__id=value(request.POST["authorFind"]))
        notes = list(chain(notesLayer,notesName,notesRegion,notesUser,notesDate,notesAuthor))
        
        findForm = FindForm()
        
        
        if request.POST["layerFind"]:
            l = Layer.objects.get(id=request.POST["layerFind"])
        else:    
            l = Layer.objects.get(id=2)
        print("*"*20)
        return  dict(layer=l,notes=notes,findForm = findForm)
    try:
        l = Layer.objects.get(name="all")
    except Layer.DoesNotExist:
        raise Http404("Vrstva neexistuje!!")
    # notes = Note.objects.filter(layer__id=l.id)
    notes = Note.objects.all()
    findForm = FindForm()    

    if "advanceFind" in request.POST:
        notes=set()
        num = 0
        query = request.POST.getlist("textFind")
        for item in query:
            if len(str(item)) > 0:
                num += len(query)
                map(notes.add,Note.objects.filter(name__icontains=value(item)))
        query = request.POST.getlist("layerFindAd")
        num += len(query)
        for item in query:
            map(notes.add,Note.objects.filter(layer__id=value(item)))
        query = request.POST.getlist("nameFindAd")
        num += len(query)
        for item in query:
            map(notes.add,Note.objects.filter(id=value(item)))
        query = request.POST.getlist("regionFindAd")
        num += len(query)
        for item in query:
            map(notes.add,Note.objects.filter(region=value(item)))
        query = request.POST.getlist("userFindAd")
        num += len(query)
        for item in query:
            map(notes.add,Note.objects.filter(participants__id=value(item)))
        if num==0:
            notes = Note.objects.all()
    return dict(layer=l,notes=notes,findForm = findForm)

@register.inclusion_tag('searchingMap.html')
def searching():
    findForm = FindForm() 
    return {'findForm': findForm}

@register.inclusion_tag('listNotesTemplate.html')
def listNotes(user):
    notes = Note.objects.filter(participants__id=user.id).order_by("-id")
    return dict(notes=notes)
    


