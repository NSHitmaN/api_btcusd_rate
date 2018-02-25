from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
import time
import requests
import datetime
import dateutil.parser
import simplejson
from rate_app.models import Record

#curl --header "X-login: newuser" --header "X-password: newpassword" "http://127.0.0.1:8000/rate/current"
def calc_avg(request):
    if request.META.__contains__('HTTP_X_LOGIN') and request.META.__contains__('HTTP_X_PASSWORD'):
        user = authenticate(username=request.META['HTTP_X_LOGIN'],password=request.META['HTTP_X_PASSWORD'])
        if user is not None:
            r = Record.objects.latest('timestamp')
            last_db_record = simplejson.dumps(r.to_dict())
            
            return HttpResponse(last_db_record, content_type='application/json')
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=400)


#curl --header "X-login: newuser" --header "X-password: newpassword" "http://127.0.0.1:8000/rate/history/?start_time=1519587514063&final_time=1519587531732"
def history(request):
    if request.META.__contains__('HTTP_X_LOGIN') and request.META.__contains__('HTTP_X_PASSWORD'):
        user = authenticate(username=request.META['HTTP_X_LOGIN'],password=request.META['HTTP_X_PASSWORD'])
        if user is not None:      
            if request.GET.__contains__('start_time'):
                start_time = int(request.GET['start_time'])
            else:
                start_time = 1514764800             ##2018-01-01T00:00:00.000000+00:00
                
            if request.GET.__contains__('final_time'):
                final_time = int(request.GET['final_time'])
            else:
                final_time = int(time.time() * 1000)
                
            
            #start_date = dateutil.parser.parse(start_date)
            #final_date = dateutil.parser.parse(final_date)
            
                
            '''if request.META.__contains__('HTTP_X_START_DATE'):
                start_date = request.META['HTTP_X_START_DATE']
            else:
                start_date = "2018-01-01T00:00:00.000000+00:00"
                
            if request.META.__contains__('HTTP_X_FINAL_DATE'):
                final_date = request.META   ['HTTP_X_FINAL_DATE']
            else:
                final_date = datetime.datetime.now().isoformat()
            '''  
            r = Record.objects.filter(timestamp__gte=start_time, timestamp__lte=final_time)
            
            all_records = []
            
            for record in r:
                all_records.append(record.to_dict())
            return HttpResponse(simplejson.dumps(all_records), content_type='application/json')
            
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=400)
        
