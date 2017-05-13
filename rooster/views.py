from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Dienst, StdDienst, Chauffeur
from django.utils import timezone
from .forms import DienstForm
from django.forms import formset_factory
import datetime
import calendar
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def api_list(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        dienst = Dienst.objects.get(pk=pk)
        serializer = DienstSerializer(dienst, many=False)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DienstSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def month_text(month):
    month_list = [
        'Leeg',
        'Januari',
        'Februari',
        'Maart',
        'April',
        'Mei',
        'Juni',
        'Juli',
        'Augustus',
        'September',
        'Oktober',
        'November',
        'December'
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
    if request.method == "POST":
        form = DienstForm(request.POST, instance=dienst)
        print('form')
        if form.is_valid():
            dienst = form.save(commit=False)
            dienst = form.save()
            print('saved')
            return redirect('dienst_detail',pk = pk)
        else:
            print('not valid')
    else:
        form = DienstForm(instance=dienst)
    return render(request, 'rooster/dienst_edit.html', {'form': form, 'dienst': dienst})

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
