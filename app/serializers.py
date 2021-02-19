"""Asset y Column Serializer"""

# Models
from app.models import Asset

# Django REST FRAMEWORK
from rest_framework import serializers


class AssetModelSerializer(serializers.ModelSerializer):
    """Circle model Serializer"""

    class Meta:
        model = Asset
        fields = (
            'timestamp',
            'name',
            'column_name',
            'column_name',
        )
