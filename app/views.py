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
import os, io, csv
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
        form = CsvModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                file = request.FILES.__copy__()
                path = file['file_name'].temporary_file_path()
                file_name = request.FILES['file_name']._get_name()
                fn = '.'.join(file_name.split('.')[:-1])
                param_file = io.TextIOWrapper(request.FILES['file_name'].file)
                data_reader = csv.DictReader(param_file)
                list_of_dict = list(data_reader)

                objs = [
                    Asset(
                        timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S%z'),
                        name=row['tag'].split('/')[2],
                        column_name=row['tag'].split('/')[3],
                        value=row['value']
                    )
                    for row in list_of_dict
                ]
                try:
                    Asset.objects.bulk_create(objs)
                    print('La información fue cargada correctamente')
                except Exception as e:
                    print(e)         

                df = pd.read_csv(path)
                df.to_parquet('./parquets/' + fn + '.parquet.gzip', compression='gzip')
                file_p = open('./parquets/' + fn + '.parquet.gzip', 'r+b')
                parquet_file = File(file_p)

                try:
                    Parquet.objects.create(file_name=parquet_file)
                    last_p = Parquet.objects.last()
                    url = last_p.file_name.url
                    os.remove('./parquets' + '/' + ''.join(os.listdir('./parquets')[-1:]))
                    context['url'] = url
                except:
                    print('error')
                form.save()
                form = CsvModelForm()
                context['form'] = form

                return render(request, 'upload.html', context)
            except Exception as e:
                print(e)
                return HttpResponse('Seems that the uploaded data did not correspond to data for the challenge, please try again :)')
    else:
        form = CsvModelForm()
    context['form'] = form
    return render(request, 'upload.html', context)
