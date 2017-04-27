from django.conf.urls import url
from rest_framework import routers
from rooster.views import DienstViewSet, ChauffeurViewSet

router = routers.DefaultRouter()
router.register(r'dienst', DienstViewSet)
router.register(r'chauffeur', ChauffeurViewSet)

urlpatterns = router.urls
