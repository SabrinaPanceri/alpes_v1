#coding: utf-8


##################################################################
### CÓDIGO DESENVOLVIDO POR SABRINA SIQUEIRA PANCERI            ##
### PROTÓTIPO DE SUA  DISSERTAÇÃO DE MESTRADO                   ##
### ESSE CÓDIGO PODE SER COPIADO, ALTERADO E DISTRIBUÍDO        ##
### DESDE QUE SUA FONTE SEJA REFERENCIADA                       ##
### PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO ATRAVÉS DO EMAIL    ##
### SABRINASPANCERI@GMAIL.COM                                   ##
##################################################################


from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    
    #abre o projeto com a página inicio1.html
    url(r'^$', 'alpes_core.views.home', name='home'),
    url(r'^similarityGroups/$', 'alpes_core.views.similarityGroups', name='Grupos de Similaridade'),
    url(r'^teses/(?P<tese_id>\d+)/$', 'alpes_core.views.teses', name='teses'),
    
    url(r'^debate/(?P<debate_id>\d+)/$', 'alpes_core.views.debate', name='debate'),
    
#     #view funcional e realizando agrupamentos - usado para o artigo sbie/2015
#     url(r'^posInicial/(?P<debate_id>\d+)/$', 'alpes_core.views.posInicial', name='posInicial'), 
    
    #URL DOS AGRUPAMENTOS - PARA REALIZAR A CLUSTERIZAÇÃO
    url(r'posInicial/(?P<debate_id>\d+)/(?P<qtdeGrupos>\d+)$', 'alpes_core.views.clusterizacao', name='clusterizacao'),
    
    
    #navegação entre as páginas
#     url(r'^index', 'alpes_core.views.index', name='index'),
#     url(r'^charts', 'alpes_core.views.charts', name='charts'),
    
       
    
    #pagina de administração do sistema
    url(r'^admin/', include(admin.site.urls)),  
)
urlpatterns += staticfiles_urlpatterns()