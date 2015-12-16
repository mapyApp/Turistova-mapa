from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turistickaMapa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^logIn/$', 'mapa.views.logIn', name='logIn'),
    url(r'^logOut/$', 'mapa.views.logOut', name='logOut'),
    url(r'^zapisdetail/(?P<zapis_id>\d+)/$', 'mapa.views.zapisDetail', name='zapisDetail'),
    url(r'^mapa/(?P<vrstva_id>\d+)/$', 'mapa.views.mapa', name='mapa'),
    url(r'^zapispridaj/$', 'mapa.views.zapisPridaj', name='zapisPridaj'),
    url(r'^profil/$', 'mapa.views.profil', name='profil'),
    url(r'^teampridaj/$', 'mapa.views.teamPridaj', name='teamPridaj'),
    url(r'^teamuprav/(?P<team_id>\d+)/$', 'mapa.views.teamUprav', name='teamUprav'),
    url(r'^napaduprav/(?P<team_id>\d+)/$', 'mapa.views.napadUprav', name='napadUprav'),
    
    

    
)
