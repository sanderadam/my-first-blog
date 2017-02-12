from django.contrib import admin
from .models import Chauffeur, Dienst, StdDienst

admin.site.register(Chauffeur)
admin.site.register(Dienst)
admin.site.register(StdDienst)
