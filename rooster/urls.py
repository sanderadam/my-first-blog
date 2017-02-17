from django.conf.urls import url
from . import views
#from django.contrib.auth import views as authviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.startpage, name='startpage'),
    url(r'^main/$', views.mainpage, name='mainpage'),
    url(r'^dienst/(?P<pk>\d+)/$', views.dienst_detail, name='dienst_detail'),
    url(r'^dienstlijst/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.dienst_list, name='dienstlijst'),
    url(r'^dienst_chauffeur/(?P<chauffeur_pk>[0-9]{1,2})/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.dienst_chauffeur, name='dienst_chauffeur'),
    url(r'^dienst/(?P<pk>\d+)/edit/$', views.dienst_edit, name='dienst_edit'),
    url(r'^diensten_toevoegen/(?P<month>[0-9]{1,2})/$', views.diensten_toevoegen, name='diensten_toevoegen'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'rooster/base_login.html'}),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^excel/$', views.download_excel, name='download_excel'),

]
# url(r'^dienst/new/$', views.dienst_new, name='dienst_new'),
#now surely updated
#url('^', include('django.contrib.auth.urls')),
#url(r'^$', views.startpage, name='startpage'),
#  url(r'^login/$', 'django.contrib.auth.views.login'),
# url(r'^logout/$', 'django.contrib.auth.views.logout'),
#url(r'^dienstlijst/$', views.dienst_list, name='dienst_list'),
#url(r'^dienst_chauffeur_all/(?P<chauffeur_pk>[0-9]{2})/$', views.dienst_chauffeur_all, name='dienst_chauffeur_all'),
