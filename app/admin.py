from django.contrib import admin

from .models import Csv, Asset, Column, Parquet

admin.site.register(Csv)
admin.site.register(Parquet)
admin.site.register(Asset)
admin.site.register(Column)
