import datetime
from rooster.models import StdDienst
#stdDienst_list = list(StdDienst.objects.all().values('date'))
stdDienst_list = StdDienst.objects.all().values('beschrijving','date','chauffeur','begintijd','eindtijd')


year = 2017
month = 1

dates_list = []

for i in range(1,31):
    for stdDienst in stdDienst_list:
        i_date = datetime.date(year,month,i)
        if(i_date.weekday()==stdDienst['date'].weekday()):
            dates_list.append(stdDienst)



