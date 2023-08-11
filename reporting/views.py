import requests
import pandas as pd
from django.shortcuts import render, HttpResponse, redirect
from sendMessage.models import Batch
from datetime import datetime
from django.core.cache import cache
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def reports(request):
    return render(request, 'reporting.html')

def systemReports(request):
    df = pd.DataFrame()
    batches = Batch.objects.all()
    for batch in batches:
        print(batch.api_dict())
        df = pd.concat([df, pd.DataFrame([batch.api_dict()])], ignore_index=True)
    print(df)
    df.to_csv('systemReport_{}.csv'.format(datetime.now()))
    messages.info(request, "Successfully downloaded System Report!")
    return redirect("reports")
    
    

def schoolReports(request):
    cached_school_data = cache.get('school_data_json')
    if cached_school_data:
        logger.info("Data fetched from cache")
        school_data = pd.DataFrame.from_dict(cached_school_data)
    else:
        logger.info("No data available in cache")
        response_API = requests.get('http://127.0.0.1:5000/get-kaggle-data/andrewmvd/us-schools-dataset?select=Private_Schools.csv')
        response_json = response_API.json()

        school_data = pd.DataFrame.from_dict(response_json)
        cache.set('school_data_json', response_json)
    selected_columns = request.POST.getlist('fieldsChecked')
    if len(selected_columns):
        school_data = school_data[selected_columns]
    school_data.to_csv('schoolReport_{}.csv'.format(datetime.now()))
    messages.info(request, "Successfully downloaded School Report!")
    return redirect("reports")
    