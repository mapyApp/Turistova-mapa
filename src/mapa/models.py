from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random


class Region(models.Model):
    name = models.CharField(max_length = 200)
    
    def __unicode__(self):
        return self.name

class Idea(models.Model):
    author = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name

# Create your models here.
class Layer(models.Model):
    name = models.CharField(max_length=300)
    color= models.CharField(max_length=100,blank=True)
    
    def save(self, *args, **kwargs):
        if self.color =="":
            self.color = self.random_color();
        super(Layer, self).save(*args, **kwargs)
        
    def random_color(self):
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r());
    
    def __unicode__(self):
        return self.name

class Note(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    region = models.ForeignKey(Region)
    author = models.ForeignKey(User,related_name="authorNote")
    participants = models.ManyToManyField(User)
    description = models.TextField()
    layer = models.ManyToManyField(Layer)
    idea = models.ManyToManyField(Idea,blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    
    
                                    
    def __unicode__(self):
        return self.name
    
class Comment(models.Model):
    author = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    text = models.TextField()
    note= models.ForeignKey(Note)
    
    def __unicode__(self):
        return self.text
    


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField("Image", upload_to="images/")
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
    

class Team(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User,related_name="authorTeam")
    participants = models.ManyToManyField(User)
    description = models.TextField()
    ideas = models.ManyToManyField(Idea,blank=True)
    
    def __unicode__(self):
        return self.name
        
class Picture(models.Model):
    note = models.ForeignKey(Note)
    name = models.CharField(max_length=20)
    description = models.TextField()
    img = models.ImageField("picture", upload_to="images/gallery")
    



    
    

    
    
    


    
    
