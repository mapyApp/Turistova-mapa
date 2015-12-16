from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random

class Napad(models.Model):
    autor = models.ForeignKey(User,related_name = "autorNapad")
    nazov = models.CharField(max_length=100)
    textovy_popis = models.TextField()
    
    def __unicode__(self):
        return self.nazov

# Create your models here.
class Vrstva(models.Model):
    nazov = models.CharField(max_length=300)
    
    def nahodnaFarba(self):
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r());
    def __unicode__(self):
        return self.nazov

class Zapis(models.Model):
    nazov = models.CharField(max_length=300)
    datum = models.DateField()
    kraj = models.CharField(max_length=300)
    autor = models.ForeignKey(User,related_name="autor")
    ucastnici = models.ManyToManyField(User)
    textovy_popis = models.TextField()
    vrstvy = models.ManyToManyField(Vrstva)
    napad = models.ManyToManyField(Napad,blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
                                    
    def __unicode__(self):
        return self.nazov
    
class DiskusnyPrispevok(models.Model):
    autor = models.ForeignKey(User)
    datum = models.DateField(auto_now=True)
    text = models.TextField()
    zapis = models.ForeignKey(Zapis)
    
    def __unicode__(self):
        return self.text
    


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    zapis = models.ManyToManyField(Zapis)
    
User.profile = property(lambda u : UserProfile.objects.get_or_create(user=u)[0])

class Team(models.Model):
    nazov = models.CharField(max_length=100)
    zakladatel = models.ForeignKey(User,related_name="autor_teamu")
    clenovia = models.ManyToManyField(User,related_name="clenovia_teamu")
    popis = models.TextField()
    napady = models.ManyToManyField(Napad,blank=True)
    
    def __unicode__(self):
        return self.nazov



    
    

    
    
    


    
    
