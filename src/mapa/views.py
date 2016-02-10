from django.shortcuts import render_to_response,redirect
from django.shortcuts import render,get_object_or_404
from models import*
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login,logout
from mapa.forms import*
from django.contrib.auth.forms import PasswordChangeForm
import logging
from django.contrib.auth import update_session_auth_hash
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404
from itertools import chain


# Create your views here.
def noteDetail(request,note_id):
    if not request.user.is_authenticated():
        return redirect("logIn")  
    note =  Note.objects.get(pk=note_id)
    discussion =  Comment.objects.filter(note=note)
    ideaForm = IdeaForm()
    ideas = Idea.objects.filter(note=note)
    if request.method=="POST":
        if "discussion" in request.POST:
            comment = Comment(author=request.user,text=request.POST["text"],note=note);
            comment.save()
        elif "idea" in request.POST:
            if request.method == 'POST':
                form = IdeaForm(request.POST)
                if form.is_valid():
                    m = form.save(commit = False)
                    m.author = request.user
                    m.save()
                    note = Note.objects.get(id=note_id)
                    note.idea.add(m)
                    note.save()
                    return redirect("noteDetail",note_id)
    return  render(request,"noteDetailTemplate.html",dict(note=note,discussion=discussion,idea=ideaForm,ideas=ideas))

def noteAdd(request):
    if not request.user.is_authenticated():
        return redirect("logIn")  
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NoteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            m = form.save(commit = False)
            m.autor = request.user
            try:
                m.lat = float(request.POST["lat"])
                m.lng = float(request.POST["lng"])
            except ValueError:
                form = NoteForm(request.POST)
                error = '<p>Nebolo zadane umiestnenie na mape</p>'
                return render(request,"zapisPridaj.html",dict(form=form,error=error))
            m.save()
            form.save_m2m()
            return redirect("noteDetail",m.id)
    # if a GET (or any other method) we'll create a blank form
    else:     
        form = NoteForm()

    return render(request, 'noteAddTemplate.html', {'form': form,})

def value(st):
    if st!= "":
        return st
    return -1

def dateFormat(post):
    print(post)
    if post != "-":
        date = post.split(".")
        return date[2]+"-"+date[1]+"-"+date[0]
    return "2000-2-2"

def map(request,layer_id=1):
    if not request.user.is_authenticated():
        return redirect("logIn")  
    if "find" in request.POST:  
        
        
      
        notesLayer= Note.objects.filter(layer__id=value(request.POST["layer"]))
        notesName = Note.objects.filter(id=value(request.POST["name"]))
        notesRegion = Note.objects.filter(region=value(request.POST["region"]))
        notesUser = Note.objects.filter(participants__id=value(request.POST["user"]))
        notesDate = Note.objects.filter(date=dateFormat(request.POST["date"]))
        notes = list(chain(notesLayer,notesName,notesRegion,notesUser,notesDate))
        
        findForm = FindForm()
        
        
        if request.POST["layer"]:
            l = Layer.objects.get(id=request.POST["layer"])
        else:    
            l = Layer.objects.get(id=1)
        return render(request,"map.html",dict(layer=l,notes=notes,findForm = findForm))
    try:
        l = Layer.objects.get(id=layer_id)
    except Layer.DoesNotExist:
        raise Http404("Vrstva neexistuje!!")
    notes = Note.objects.filter(layer=l)
    findForm = FindForm()    
    return render(request,"map.html",dict(layer=l,notes=notes,findForm = findForm))

def logIn(request):
    if request.user.is_authenticated():
        return redirect("map",1) 
    if(request.POST):
        name = request.POST['user']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("map",1)
            
        else:
            return render(request,"logIn.html",{"errorLog":"Boli zadane zle udaje"})
    else:
        return render(request,"logIn.html",{})

def logOut(request):
    logout(request)
    return redirect("logIn");

def profil(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
    if request.method == "POST":
        if "other" in request.POST:
            form1 = UserProfilForm(request.POST,request.FILES,instance=request.user.profile)
            if form1.is_valid():
                instance = form1.save(commit=False)
                instance.autor = request.user
                instance.save()
                print("image je ok")
            else:
                print("inavalidny image")
        if "nameEmail" in request.POST:
            form2 = UserForm(request.POST,instance = request.user)
            if form2.is_valid():
                f2 =form2.save()
        if "password" in request.POST:
            form3 = PasswordChangeForm(user=request.user,data=request.POST)
            if form3.is_valid():
                form3.save()
                update_session_auth_hash(request,request.user)
        return redirect("profil") 
   #u = UserProfile.objects.get(id=1)
    notes = Note.objects.filter(participants__id=request.user.id)
    form1 = UserProfilForm(instance = request.user.profile)
    form2 = UserForm(instance = request.user)
    form3 = PasswordChangeForm(request.user)
    
    return render(request,"profilTemplate.html",dict(form1=form1,form2=form2,form3= form3,profil=request.user.profile,notes=notes))

def teamPridaj(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeamForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            m = form.save(commit = False)
            m.zakladatel = request.user
            m.save()
            teamVytvoreny = True
            return redirect("teamUprav",teamVytvoreny)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeamForm()
    return render(request,"teamPridaj.html",dict(form = form))

def teamUprav(request,team_id,teamVytvoreny=False):
    if not request.user.is_authenticated():
        return redirect("logIn")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        team = Team.objects.get(pk=team_id)
        form = TeamForm(request.POST,instance = team)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            m = form.save()
            teamSprava = "Team bol upraveny"
            return render(request,"teamUprav.html",dict(form = form,id=team_id,sprava = teamSprava))

    # if a GET (or any other method) we'll create a blank form
    else:
        team = Team.objects.get(pk=team_id)
        form = TeamForm(instance = team)
    return render(request,"teamUprav.html",dict(form = form,id=team_id))


def napadUprav(request):
    pass

def searching(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
    notes = []
    if "find" in request.POST:
        notesLayer= Note.objects.filter(layer__id=value(request.POST["layer"]))
        notesName = Note.objects.filter(id=value(request.POST["name"]))
        notesRegion = Note.objects.filter(region=value(request.POST["region"]))
        notesUser = Note.objects.filter(participants__id=value(request.POST["user"]))
        notesDate = Note.objects.filter(date=dateFormat(request.POST["date"]))
        notes = list(chain(notesLayer,notesName,notesRegion,notesUser,notesDate))
    form = FindForm()
    return render(request,"searchingTemplate.html",dict(form=form,notes=notes))

