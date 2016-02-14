from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls.static import static
from settings import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turistickaMapa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'mapa.views.logIn', name='logIn'),
    url(r'^logout/$', 'mapa.views.logOut', name='logOut'),
    url(r'^notedetail/(?P<note_id>\d+)/$', 'mapa.views.noteDetail', name='noteDetail'),
   ## url(r'^map/(?P<layer_id>\d+)/$', 'mapa.views.map', name='map'),
    url(r'^noteadd/$', 'mapa.views.noteAdd', name='noteAdd'),
     url(r'^searching/$', 'mapa.views.searching', name='searching'),
    url(r'^profil/$', 'mapa.views.profil', name='profil'),
    url(r'^teamChange/(?P<team_id>\d+)/$', 'mapa.views.teamChange', name='teamChange'),
    url(r'^notedetailpaginator/$', 'mapa.views.noteDetailPaginator', name='noteDetailPaginator'),
   
    
)