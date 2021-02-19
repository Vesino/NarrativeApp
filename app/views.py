from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files import File
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Django Rest Framework
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status

# Models
from .models import Csv, Asset, Column, Parquet

# Serializers
from app.serializers import AssetModelSerializer

# Forms
from .forms import CsvModelForm, AssetForm

# Utilities
import os, io, csv
import json
from datetime import datetime
from collections import Counter

# pandas
import pandas as pd
import numpy as np

# Plotly
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go

# Django pandas
from django_pandas.io import read_frame

# API services
from app.services import get_assets


def index(request):
    return render(request, 'index.html', {})


def upload(request):
    """ View which handles all the proces of the data sent it for any user

    This view receive any csv file corresponding to the data challenge, otherwise it won't process it
    """
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
                except:
                    messages.warning(request, 'Something went wrong while uploaded data :(')
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
                messages.success(request, 'Data uploaded')          
            except Exception as e:
                print(e)
                return HttpResponse('Seems that the uploaded data did not correspond to data for the challenge, please try again :)')
    else:
        form = CsvModelForm()
    context['form'] = form
    return render(request, 'upload.html', context)


def list_files(request):
    """View for list all the csv uploaded and the parquets files generated"""
    context = {}
    try:
        parquets = Parquet.objects.all()
        csvs = Csv.objects.all()
        context.update({
            'parquets':parquets,
            'csvs':csvs
        })
        return render(request, 'listfiles.html', context)
    except ObjectDoesNotExist:
            messages.info(request, "You do not have any file yet")
    return render(request, 'listfiles.html', context)

# Consume API

def data_visualization(request):
    """
    View which handles the consume of our API
    """
    context = {}
    if request.method == 'POST':
        form = AssetForm(request.POST or None)
        if form.is_valid():
            
            asset = request.POST['asset_name']
            day = request.POST['date'].split('/')[0]
            month = request.POST['date'].split('/')[1]
            year = request.POST['date'].split('/')[2]
            assets_list = get_assets(asset, year, month, day)

            records = [line for line in assets_list['assets']]
            columnas = [rec['column_name'] for rec in records]
            counts = Counter(columnas)
            counts = dict(counts)
            keys = list(counts.keys())
            values = list(counts.values())
            fig = go.Figure([go.Bar(x=keys, y=values)], layout_title_text="Number of columns by {} on the date {}".format(asset, request.POST['date']))
            plot_div = plot(fig, output_type='div')
            context['plot_div'] = plot_div
            context['asset'] = asset
            context['form'] = form
            messages.info(request, 'API consumed')
    else:
        form = AssetForm()
    context['form'] = form
    return render(request, 'datavisual.html', context)


# API
class AssetViewSet(viewsets.ModelViewSet):
    """ViewSet for Asset
    
    This ViewSet is in charge of all the request related to Asset model
    """
    serializer_class = AssetModelSerializer
    def get_queryset(self):
        """In get request only retreive data if asset, year, month and day are given

        """
        queryset = Asset.objects.all()
        if self.action == 'list':
            asset = self.request.query_params.get('asset', None)
            year = self.request.query_params.get('year', None)
            month = self.request.query_params.get('month', None)
            day = self.request.query_params.get('day', None)
            if asset is not None and year is not None and month is not None and day is not None:
                    queryset = queryset.filter(timestamp__year=year).filter(timestamp__month=month).filter(timestamp__day=day).filter(name=asset)
        return queryset
        

