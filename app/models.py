from django.db import models
from django.core.validators import FileExtensionValidator

# Pandas Django
from django_pandas.managers import DataFrameManager


ASSET_CHOICES = (
    ('WTG01', 'WTG01'),
    ('WTG02', 'WTG02'),
    ('WTG03', 'WTG03'),
    ('WTG04', 'WTG04'),
    ('WTG05', 'WTG05'),
    ('WTG06', 'WTG06'),
    ('WTG07', 'WTG07'),
    ('WTG08', 'WTG08'),
    ('WTG09', 'WTG09'),
    ('WTG10', 'WTG10'),
    ('WTG11', 'WTG11'),
    ('WTG12', 'WTG12'),
    ('WTG13', 'WTG13'),
    ('WTG14', 'WTG14'),
    ('WTG15', 'WTG15'),
    ('WTG16', 'WTG16'),
    ('WTG17', 'WTG17'),
)

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')

    def __str__(self):
        return f"{self.file_name}"

class Parquet(models.Model):
    file_name = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['gzip'])])
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file_name}'


class Asset(models.Model):
    timestamp = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=20, choices=ASSET_CHOICES, null=True, blank=True)
    column_name = models.CharField(max_length=100, null=True, blank=True)
    #since the nature of colun value on csv for challenge is not consistent with a single type of value (ej: int, float)
    #value is set as charfield and in the view we could processed and transform it as int or float
    value = models.CharField(max_length=50, null=True, blank=True)

    objects = DataFrameManager()

    def __str__(self):
        return f'{self.name}, {self.column_name}'


class Column(models.Model):
    timestamp = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    asset_name = models.CharField(max_length=20, choices=ASSET_CHOICES, null=True, blank=True)
    #since the nature of colun value on csv for challenge is not consistent with a single type of value (ej: int, float)
    #value is set as charfield and in the view we could processed and transform it as int or float
    value = models.CharField(max_length=50, null=True, blank=True)

    objects = DataFrameManager()
    
    def __str__(self):
        return f'{self.name}, {self.asset_name}'
    
