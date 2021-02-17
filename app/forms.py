from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
# Models
from .models import Csv, Parquet

class CsvModelForm(forms.ModelForm):
    file_name = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])

    class Meta:
        model = Csv
        fields = ('file_name',)
