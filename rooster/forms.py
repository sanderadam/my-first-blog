from django import forms
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from .models import Dienst, Chauffeur


class DienstForm(forms.ModelForm):

    class Meta:
        model = Dienst
        fields = ('beschrijving', 'chauffeur', 'date', 'begintijd','eindtijd')
        widgets = {
            #Use localization and bootstrap 3
            'begintijd': TimeWidget(attrs={'id':"begintijd"}, usel10n = True, bootstrap_version=3),
            'eindtijd': TimeWidget(attrs={'id':"eindtijd"}, usel10n = True, bootstrap_version=3)
        }


class SimpelForm(forms.ModelForm):

    class Meta:
        model = Dienst
        fields = ('beschrijving',)





