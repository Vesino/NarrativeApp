from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File

# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Models
from .models import Csv, Asset, Column, Parquet

# Serializers
from app.serializers import AssetListSerializer, CreateAssetSerializer

# Forms
from .forms import CsvModelForm

# Utilities
import csv
import os
from datetime import datetime

# pandas
import pandas as pd
import numpy as np

# Django pandas
from django_pandas.io import read_frame


def index(request):
    return render(request, 'index.html', {})

def upload(request):
    context = {}
    if request.method == 'POST':
        form = CsvModelForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES.__copy__()
            path = file['file_name'].temporary_file_path()
            df = pd.read_csv(path)
            df.to_parquet('./parquets/df.parquet.gzip', compression='gzip')
            file_p = open('./parquets/df.parquet.gzip', 'r+b')
            parquet_file = File(file_p)
            try:
                Parquet.objects.create(file_name=parquet_file)
                last_p = Parquet.objects.last()
                url = last_p.file_name.url
                context['url'] = url
            except:
                raise Exception("Something went wrong")
            os.remove('./parquets' + '/' + ''.join(os.listdir('./parquets')[-1:]))
            try:
                with open(path, 'r') as file:
                    reader = csv.reader(file)
                    for i, row in enumerate(reader):
                        if i==0:
                            pass
                        else:
                            # row is a list containing data for data-challenge
                            # [0] stands for column timestamp 
                            # [1] stands for column tag
                            # [2] stands for column value 
                            asset = row[1].split('/')[2]
                            column = row[1].split('/')[3]
                            value = row[2]
                            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S%z')
                            # timestamp = row[0]
                            if len(asset) > 5:
                                print("This is not an NarrativeWive Asset")
                                return HttpResponse("This is not a data set for the challenge")
                            try:
                                asset_content(timestamp,asset,column,value)
                            except:
                                return HttpResponse('No fue posible guardar el dato como date time')
                            # column_content(column,asset,value)

                            # print(f'This is the asset {asset}, this is the column {column}, this is the value {value}, the timestamp is {timestamp}')
                           
            except:
                return HttpResponse("This is not a data set for the challenge Narrative Wave please upload one of them")
            form.save()
            form = CsvModelForm()
            context['form'] = form
            # The next logic handles the process data of tha last uploaded csv file
            # just if the file is from the data challenge, otherwise it'll return an HttpResponse("This is not a data set for the challenge Narrative Wave please upload one of them")
            # obj = Csv.objects.last()
            # import pdb; pdb.set_trace()
            # to_parquet(obj_to_parquet.file_name.path)
            
    else:
        form = CsvModelForm()
        context['form'] = form
    
    return render(request, 'upload.html', context)

def asset_content(timestamp,asset,column,value):
    return Asset.objects.create(
        timestamp=timestamp, 
        name=asset,
        column_name=column,
        value=value
    )