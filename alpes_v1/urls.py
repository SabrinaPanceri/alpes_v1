#coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    
    #abre o projeto com a página index.html
    url(r'^$', 'alpes_core.views.home', name='home'),
    url(r'^(?P<tese_id>\d+)/$', 'alpes_core.views.teses', name='teses'),
    url(r'^debate/(?P<debate_id>\d+)/$', 'alpes_core.views.debate', name='debate'),
    
    #navegação entre as páginas
    url(r'^index', 'alpes_core.views.index', name='index'),
    url(r'^charts', 'alpes_core.views.charts', name='charts'),
    
    

    
    
    #pagina de administração do sistema
    url(r'^admin/', include(admin.site.urls)),  
)
urlpatterns += staticfiles_urlpatterns()