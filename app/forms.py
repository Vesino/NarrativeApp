from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator

# Utils
import datetime

# Models
from .models import Csv

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
    ('WTG17', 'WTG17')
)

class CsvModelForm(forms.ModelForm):
    file_name = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])

    class Meta:
        model = Csv
        fields = ('file_name',)


class AssetForm(forms.Form):
    asset_name = forms.ChoiceField(choices = ASSET_CHOICES, label="Chose one Asset", initial='', widget=forms.Select(), required=True)
    date = forms.DateTimeField(required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'dd/mm/yyyy'}), validators=[RegexValidator(r'[\d]{4}')])