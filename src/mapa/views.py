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
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger


# Create your views here.
def noteDetail(request,note_id):
    if not request.user.is_authenticated():
        return redirect("logIn")
    note =  Note.objects.get(pk=note_id)
    discussion =  Comment.objects.filter(note=note)
    ideaForm = IdeaForm()
    ideas = Idea.objects.filter(note=note)
    gallery = Image.objects.filter(note=note)
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
                    form.save_m2m()
                    note = Note.objects.get(id=note_id)
                    note.idea.add(m)
                    note.save()
                    return redirect("noteDetail",note_id)
    return  render(request,"noteDetailTemplate.html",dict(note=note,discussion=discussion,idea=ideaForm,ideas=ideas, gallery=gallery))

def noteAdd(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
    
    if request.method == 'POST':
        if "noteAdd" in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                m = form.save(commit = False)
                m.author = request.user
                try:
                    m.lat = float(request.POST["lat"])
                    m.lng = float(request.POST["lng"])
                except ValueError:
                    pass
                m.save()
                form.save_m2m()
                layerAll = Layer.objects.filter(name="all")
                if(len(layerAll)==0):
                    layerAll = Layer.objects.get(name="all")
                else:
                    layerAll = layerAll[0]
                m.layer.add(layerAll)
                m.save()
                return redirect("noteDetail",m.id)
    else:
        form = NoteForm()
    if "find" in request.POST:
        form = NoteForm()
    return render(request, 'noteAddTemplate.html', {'form': form,})

def noteDetailPaginator(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
    notes_set = Note.objects.all().order_by("-id")
    paginator = Paginator(notes_set, 1) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notes = paginator.page(paginator.num_pages)
    try:
        note =  notes[0]
    except IndexError:
        raise Http404("treba vytvorit aspon 1 zapis")
    discussion =  Comment.objects.filter(note=note)
    gallery = Image.objects.filter(note=note)
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
    return  render(request,"noteDetailPaginatorTemplate.html",dict(notes=notes,
                                                                    note=note,
                                                                    discussion=discussion,
                                                                    idea=ideaForm,
                                                                    ideas=ideas,
                                                                    gallery=gallery))


def logIn(request):
    logger = logging.getLogger(__name__)
    logger.info(request.META['HTTP_HOST'])
    if request.user.is_authenticated():
        return redirect("profil")
    if(request.POST):
        name = request.POST['user']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("profil")
            
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
    
    if "nameEmail" in request.POST:
        form1 = UserForm(request.POST,instance = request.user)
        if form1.is_valid():
            m =form1.save()
    else:
        form1 = UserForm(instance = request.user)
    
    if "password" in request.POST:
        form2 = PasswordChangeForm(user=request.user,data=request.POST)
        if form2.is_valid():
            form2.save()
            update_session_auth_hash(request,request.user)
    else:
        form2 = PasswordChangeForm(request.user)
        
    if "teamAdd" in request.POST:
        teamForm = TeamForm(request.POST)
        if teamForm.is_valid():
            m = teamForm.save(commit = False)
            m.author = request.user
            m.save()
            teamForm.save_m2m()
            return redirect("teamChange", m.id)
    else:
        teamForm = TeamForm()
       
    if "find" in request.POST:
        form1 = UserForm(instance = request.user)
        form2 = PasswordChangeForm(request.user)
        teamForm = TeamForm()
    teams = Team.objects.filter(author=request.user)
    notes = Note.objects.filter(author=request.user)
    teamsMember = Team.objects.filter(participants=request.user)
    print(teamsMember)
    ideas =set()
    for item in teamsMember:
        map(ideas.add,Idea.objects.filter(team=item))
    print(ideas)   
    return render(request,"profilTemplate.html",dict(form1=form1,
                                                     form2=form2,
                                                     teamForm=teamForm,
                                                     teams=teams,
                                                     notes=notes,ideas=ideas))



def teamChange(request,team_id):
    if not request.user.is_authenticated():
        return redirect("logIn")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if "updateTeam" in request.POST:
            print("update")
            
            team = Team.objects.get(pk=team_id)
            form = TeamForm(request.POST,instance = team)
        # check whether it's valid:
            if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
                m = form.save()
                return render(request,"teamChangeTemplate.html",dict(form = form,id=team_id))
               

    # if a GET (or any other method) we'll create a blank form
    else:
        team = Team.objects.get(pk=team_id)
        form = TeamForm(instance = team)
    return render(request,"teamChangeTemplate.html",dict(form = form,id=team_id))


def noteChange(request,note_id):
    if not request.user.is_authenticated():
        return redirect("logIn")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if "updateNote" in request.POST:
            note = Note.objects.get(pk=note_id)
            form = NoteForm(request.POST,instance = note)
        # check whether it's valid:
            if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
                m = form.save()
                return render(request,"noteChangeTemplate.html",dict(form = form,note=note))
               

    # if a GET (or any other method) we'll create a blank form
    else:
        note = Note.objects.get(pk=note_id)
        form = NoteForm(instance = note)
    if "find" in request.POST:
        note = Note.objects.get(pk=note_id)
        form = NoteForm(instance = note)
    return render(request,"noteChangeTemplate.html",dict(form = form,note=note))



def value(st):
    if st!= "":
        return st
    return-1

def dateFormat(post):
    if post != ("-"):
        date = post.split(".")
        return date[2]+"-"+date[1]+"-"+date[0]
    return "2000-2-2"

def searching(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
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
        
    form = FindFormAdvance()
    return render(request,"searchingTemplate.html",dict(form=form,notes=notes))

def ideaDetail(request,idea_id):
    if not request.user.is_authenticated():
        return redirect("logIn")
    idea = Idea.objects.get(id=idea_id)
    return render(request,"ideaDetailTemplate.html",dict(idea =idea))
