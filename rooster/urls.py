from django.conf.urls import url, include
from . import views
from django.contrib.auth.models import User
#from django.contrib.auth import views as authviews
from django.contrib.auth import views as auth_views
from rest_framework import routers, serializers, viewsets
from .models import Dienst

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = Dienst.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^$', views.startpage, name='startpage'),
    url(r'^main/$', views.mainpage, name='mainpage'),
    url(r'^dienst/(?P<pk>\d+)/$', views.dienst_detail, name='dienst_detail'),
    url(r'^dienstlijst/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.dienst_list, name='dienstlijst'),
    url(r'^dienst_chauffeur/(?P<chauffeur_pk>[0-9]{1,2})/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.dienst_chauffeur, name='dienst_chauffeur'),
    url(r'^dienst/(?P<pk>\d+)/edit/$', views.dienst_edit, name='dienst_edit'),
    url(r'^diensten_toevoegen/(?P<month>[0-9]{1,2})/$', views.diensten_toevoegen, name='diensten_toevoegen'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'rooster/base_login.html'}),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'rooster/base_logout.html'}),
    url(r'^excel/$', views.download_excel, name='download_excel'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-list/(?P<pk>\d+)/', views.api_list, name='api-list')
]
# url(r'^dienst/new/$', views.dienst_new, name='dienst_new'),
#now surely updated
#url('^', include('django.contrib.auth.urls')),
#url(r'^$', views.startpage, name='startpage'),
#  url(r'^login/$', 'django.contrib.auth.views.login'),
# url(r'^logout/$', 'django.contrib.auth.views.logout'),
#url(r'^dienstlijst/$', views.dienst_list, name='dienst_list'),
#url(r'^dienst_chauffeur_all/(?P<chauffeur_pk>[0-9]{2})/$', views.dienst_chauffeur_all, name='dienst_chauffeur_all'),
