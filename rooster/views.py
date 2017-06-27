# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Dienst, StdDienst, Chauffeur
from django.utils import timezone
from .forms import DienstForm
from django.forms import formset_factory, modelform_factory, modelformset_factory
import datetime
import calendar
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy
from django.core.mail import send_mail
import locale
from django.db.models import Q
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

locale.setlocale(locale.LC_TIME, "nl_NL")

def month_text(month):
    month_list = [
        'Leeg',
        'januari',
        'februari',
        'maart',
        'april',
        'mei',
        'juni',
        'juli',
        'augustus',
        'september',
        'oktober',
        'november',
        'december'
    ]
    return month_list[month]

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)


def make_months():
    today = datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)

    month_dates = [
        add_months(today,-1),
        today,
        add_months(today,1)
    ]

    month_texts = []
    month_numbers = []
    for date in month_dates:
        month_texts.append(month_text(date.month))
        month_numbers.append(str(date.year) + "/" + '{:02d}'.format(date.month) + "/")

    return zip(month_texts, month_numbers)

@login_required
def mainpage(request):
    chauffeur = Chauffeur.objects.get(user_id=request.user)
    zipdates = make_months()

    context = {
        'chauffeur':chauffeur,
        'zipdates':zipdates
    }

    return render(request,'rooster/mainpage.html',context)

@login_required
def dienst_edit(request, pk):
    dienst = get_object_or_404(Dienst, pk=pk)

    dienst_old = deepcopy(dienst)

    if request.method == "POST":
        form = DienstForm(request.POST, instance=dienst)
        print('form')
        if form.is_valid():

            dienst = form.save(commit=False)
            dienst = form.save()

            # Send email here

            if (dienst_old.chauffeur.pk != dienst.chauffeur.pk or
                dienst_old.date != dienst.date or
                dienst_old.begintijd != dienst.begintijd or
                dienst_old.eindtijd != dienst.eindtijd or
                dienst_old.comments != dienst.comments or
                dienst_old.overname != dienst.overname
                ):

                if dienst_old.chauffeur.pk == dienst.chauffeur.pk:
                    emails = ['startvof@gmail.com',
                              dienst_old.chauffeur.email]
                    line3 = ""
                else:
                    emails = ['startvof@gmail.com',
                              dienst_old.chauffeur.email,
                              dienst.chauffeur.email]
                    line3 = " en " + dienst.chauffeur.naam

                line1 = 'Voor wijziging: {0} {1} door {2} van {3} tot {4}' \
                        .format(
                        dienst_old.beschrijving,
                        dienst_old.date.strftime('%d %B %Y'),
                        dienst_old.chauffeur.naam,
                        dienst_old.begintijd.strftime('%H:%M'),
                        dienst_old.eindtijd.strftime('%H:%M')
                        )

                line2 = 'Na wijziging:   {0} {1} door {2} van {3} tot {4}' \
                        .format(
                        dienst.beschrijving,
                        dienst.date.strftime('%d %B %Y'),
                        dienst.chauffeur.naam,
                        dienst.begintijd.strftime('%H:%M'),
                        dienst.eindtijd.strftime('%H:%M')
                        )


                body = """
                Beste {0}{1},

                Er is een dienst wijziging binnen gekomen in het start systeem. De wijziging is als volgt:

                {2}
                {3}

                Veel succes met de dienst, en stuur ons graag een mailtje als er iets niet klopt.

                Bedankt, Sander en Mark

                """.format(
                    dienst_old.chauffeur.naam,
                    line3,
                    line1,
                    line2
                )





                send_mail("Rooster wijziging",
                          body,
                          "Start Rooster Systeem <noreply@mg.startassistentie.nl>",
                          emails
                          )

                # End email


            #return redirect('dienst_detail',pk = pk)
            return redirect('/dienstlijst/{0}/{1}/#diensten'.format(str(dienst.date.year),'{:02d}'.format(dienst.date.month)))


        else:
            print('not valid')
    else:
        form = DienstForm(instance=dienst)


    context = {
                'backlink': '{0}/{1}/#diensten'.format(str(dienst.date.year),'{:02d}'.format(dienst.date.month))

    }

    return render(request, 'rooster/dienst_edit.html', {'form': form, 'dienst': dienst, 'context':context})


@login_required
def weekend(request):

    fields = ('beschrijving', 'chauffeur', 'date','begintijd','eindtijd','overname')
    WeekendFormset = modelformset_factory(Dienst, fields = fields, extra=0)

    if request.method == "POST":
        print('Received POST formset')
        formset = WeekendFormset(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:
                print(form)
                form.save()
            return redirect('/weekend_weergeven/#diensten')
        else:
            print('not valid')
    else:
        print('go')
        # Make formset

        # Find weekend
        today = datetime.datetime.now()
        date = today + datetime.timedelta(5 - today.weekday())
        date = datetime.date(2017,7,8)

        #WeekendForm = modelform_factory(Dienst, fields = fields )
        formset = WeekendFormset(queryset = Dienst.objects.filter(Q(date=date) | Q(date=date + datetime.timedelta(days=1))).exclude(beschrijving='Zondag nacht'))
        #form = WeekendForm(initial = dienst_chauffeur)

        context = {
            'datum': date.strftime('%d %B %Y'),
            'zipdates': make_months(), 
            'formset': formset
        }
        return render(request,'rooster/weekend.html',context)


@login_required
def weekend_weergeven(request):
    zipdates = make_months()
    today = datetime.datetime.now()
    date = today + datetime.timedelta(5 - today.weekday())
    date = datetime.date(2017,7,8)

    diensten = Dienst.objects.filter(Q(date=date) | Q(date=date + datetime.timedelta(days=1))).exclude(beschrijving='Zondag nacht')

    context = {
            'datum':date.strftime('%d %B %Y'),
            'diensten':diensten,
            'zipdates':zipdates,
        }

    print(context['zipdates'])

    return render(request,'rooster/weekend_weergeven.html',context)


@login_required
def diensten_toevoegen(request, month):
    stdDienst_list = list(StdDienst.objects.all().values('beschrijving','date','chauffeur','begintijd','eindtijd'))
    year = 2017
    month = int(month)
    days_in_month = calendar.monthrange(year,month)[1]
    dates_list = []

    for i in range(1,days_in_month+1):
        for stdDienst_i in stdDienst_list:
            i_date = datetime.date(year,month,i)
            if(i_date.weekday()==stdDienst_i['date'].weekday()):
                stdDienst_i['date'] = i_date
                stdDienst_i = dict(stdDienst_i)
                dates_list.append(stdDienst_i)

    DienstlijstFormset = formset_factory(DienstForm, extra=0)
    if request.method == "POST":
        print('Received POST formset')
        formset = DienstlijstFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                print(form)
                form.save()
            return redirect('diensten_toevoegen', month=month)
        else:
            print('not valid')
    else:
        print('go')
        print(dates_list)
        formset = DienstlijstFormset(initial = dates_list)
    return render(request,'rooster/diensten_toevoegen.html', {'formset': formset})

def startpage(request):
    if request.user.is_authenticated():
        return mainpage(request)
    else:
        return render(request, 'rooster/startpage.html', {'user':request.user})


@login_required
def dienst_list(request, year, month):
    diensten = Dienst.objects.filter(date__year=year).filter(date__month=month).order_by('date','begintijd')
    print('list')

    chauffeur = Chauffeur.objects.get(user_id=request.user)
    zipdates = make_months()

    context = {
        'chauffeur':chauffeur,
        'zipdates':zipdates,
        'diensten': diensten,
        'year': year,
        'month': month,
        'month_text': month_text(int(month)),
    }


    return render(request, 'rooster/dienst_list.html', context)

@login_required
def dienst_chauffeur(request, chauffeur_pk, year, month):
    diensten = Dienst.objects.filter(chauffeur = chauffeur_pk).filter(date__year=year).filter(date__month=month).order_by('date','begintijd')
    chauffeur = Chauffeur.objects.get(pk = chauffeur_pk)

    zipdates = make_months()

    context = {
        'chauffeur':chauffeur,
        'zipdates':zipdates,
        'diensten': diensten,
        'year': year,
        'month': month,
        'month_text': month_text(int(month)),
    }

    return render(request, 'rooster/dienst_chauffeur.html', context)



@login_required
def dienst_detail(request, pk):
    dienst = get_object_or_404(Dienst, pk=pk)
    chauffeur = dienst.chauffeur

    zipdates = make_months()

    context = {
        'chauffeur':chauffeur,
        'zipdates':zipdates,
        'dienst': dienst,
    }

    return render(request, 'rooster/dienst_detail.html', {'dienst': dienst})

def login_page(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...

@login_required
def download_excel(request,year,month):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mymodel.xlsx"'
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})


    # add a worksheet
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Total')

    #query
    diensten = Dienst.objects.filter(date__year=year).filter(date__month=month).order_by('date','begintijd')

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0


    # Iterate over the data and write it out row by row.
    # date month description driver length percentage
    for dienst in diensten:
        worksheet.write(row, col,     dienst.date)
        worksheet.write(row, col+1,   dienst.beschrijving)
        worksheet.write(row, col+2,   dienst.chauffeur.naam)
        worksheet.write(row, col+3,   dienst.begintijd)
        worksheet.write(row, col+4,   dienst.eindtijd)
        worksheet.write(row, col+5,   dienst.dienst_duur())
        worksheet.write(row, col+6,   dienst.feestdagen)

        #worksheet.write(row, col+1,   dienst['chauffeur'])

        row += 1

    #beschrijving = models.CharField(max_length=200)
    #comments = models.TextField
    #chauffeur = models.ForeignKey('Chauffeur')
    #date = models.DateField()
    #begintijd = models.TimeField()
    #eindtijd = models.TimeField()




    # use xlsxwriter routines to create the worksheet

    # now write it out
    workbook.close()
    return response

@login_required
def overname_diensten(request):
    diensten = Dienst.objects.filter(overname=True).order_by('date','begintijd')

    zipdates = make_months()

    context = {
        'zipdates':zipdates,
        'diensten': diensten,

    }

    return render(request, 'rooster/dienst_overname.html', context)

@login_required
def weekoverzicht(request):
    diensten = StdDienst.objects.order_by('date','begintijd')
    zipdates = make_months()
    context = {
        'zipdates':zipdates,
        'diensten': diensten,

    }

    return render(request, 'rooster/weekoverzicht.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('startpage')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'rooster/password2.html', {
        'form': form
    })
