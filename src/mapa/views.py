from django.shortcuts import render_to_response,redirect
from django.shortcuts import render,get_object_or_404
from models import*
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login,logout
from mapa.forms import*
from django.contrib.auth.forms import AdminPasswordChangeForm
import logging
# Create your views here.
def zapisDetail(request,zapis_id):
    if not request.user.is_authenticated():
        return redirect("logIn")
    zapis =  Zapis.objects.get(pk=zapis_id)
    diskusia =  DiskusnyPrispevok.objects.filter(zapis=zapis)
    napad = NapadForm()
    if request.method=="POST":
        if "diskusia" in request.POST:
            diskusnyPrispevok = DiskusnyPrispevok(autor=request.user,text=request.POST["text"],zapis=zapis);
            diskusnyPrispevok.save()
        elif "napad" in request.POST:
            if request.method == 'POST':
                form = NapadForm(request.POST)
                if form.is_valid():
                    m = form.save(commit = False)
                    m.autor = request.user
                    m.save()
                    return redirect("zapisDetail",zapis_id)
            
                
    
    return  render(request,"zapisDetail.html",dict(zapis=zapis,diskusia=diskusia,napad=napad))

def zapisPridaj(request):
    if not request.user.is_authenticated():
        return redirect("logIn")
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ZapisForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            m = form.save(commit = False)
            m.autor = request.user
            m.save()
            return redirect("zapisDetail",m.id)

    # if a GET (or any other method) we'll create a blank form
    else:     
        form = ZapisForm()

    return render(request, 'zapisPridaj.html', {'form': form,})
    

def mapa(request,vrstva_id):
    if not request.user.is_authenticated():
        return redirect("logIn")
    vrstva = Vrstva.objects.raw("select * from mapa_vrstva where id="+vrstva_id+";")[0]
    zapisy = Zapis.objects.filter(vrstvy__id=vrstva_id)
    return render(request,"mapa.html",dict(vrstva=vrstva,zapisy=zapisy))

def logIn(request):
    if request.user.is_authenticated():
        return redirect("mapa")
    if(request.POST):
        meno = request.POST['user']
        heslo = request.POST['password']
        user = authenticate(username=meno, password=heslo)
        if user is not None:
            login(request, user)
            return redirect("mapa")
            
        else:
            return render(request,"logIn.html",{"errorLog":"Boli zadane zle udaje"})
    else:
        return render(request,"logIn.html",{})

def logOut(request):
    logout(request)
    return redirect("logIn");

def profil(request):
    if not request.user.is_authenticated():
        return redirect("logIn.html")
    if request.method == "POST":
        form1 = UserProfilForm(request.POST,instance = request.user.profile)
        if form1.is_valid():
            f1 =form1.save()
            form2 = UserForm(request.POST,instance = request.user)
            form3 = AdminPasswordChangeForm(request.user,request.POST)
            if form2.is_valid():
                f2 =form2.save()
                form3 = AdminPasswordChangeForm(request.user,request.POST)
                if form3.is_valid():
                    form3.save()
                    return redirect("mapa")
        
    profile = request.user.profile
    form1 = UserProfilForm(instance = profile)
    form2 = UserForm(instance = request.user)
    form3 = AdminPasswordChangeForm(request.user)
    
    return render(request,"profil.html",dict(form1=form1,form2=form2,form3= form3))

def teamPridaj(request):
    if not request.user.is_authenticated():
        return redirect("logIn.html")
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
        return redirect("logIn.html")
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

def napadPridaj(request):
    if not request.user.is_authenticated():
        return redirect("logIn.html")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NapadForm(request.POST)
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
    else:
        
        form = NapadForm()
    return render(request,"napadPridaj.html",dict(form = form))

def napadUprav(request):
    pass
