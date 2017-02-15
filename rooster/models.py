from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Dienst(models.Model):
    beschrijving = models.CharField(max_length=200)
    comments = models.TextField
    chauffeur = models.ForeignKey('Chauffeur')
    date = models.DateField()
    begintijd = models.TimeField()
    eindtijd = models.TimeField()

    def __str__(self):
        return self.beschrijving + " " + self.date.strftime("%Y-%m-%d")

    def dienst_duur(self):
        bt = datetime.datetime(2017,1,1,self.begintijd.hour, self.begintijd.minute, self.begintijd.second)
        et = datetime.datetime(2017,1,1,self.eindtijd.hour, self.eindtijd.minute, self.eindtijd.second)
        td = et - bt
        if td < datetime.timedelta(0,0,0):
            td = td + datetime.timedelta(1,0,0)
        td_sec = td.total_seconds()
        hours = td_sec // 3600
        td_sec = td_sec - (hours * 3600)
        # minutes
        minutes = td_sec // 60
        return( '{0:1.0f}'.format(hours) + ":" + '{0:1.0f}'.format(minutes).zfill(2))
        #+str(":")+str(minutes))
        # result: 3:43:40
        # return str(td)



class Chauffeur(models.Model):
    naam = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.naam

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Chauffeur.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.chauffeur.save()

class StdDienst(models.Model):
    beschrijving = models.CharField(max_length=200)
    comments = models.TextField
    chauffeur = models.ForeignKey('Chauffeur')
    date = models.DateField()
    begintijd = models.TimeField()
    eindtijd = models.TimeField()

    def __str__(self):
        return self.beschrijving
