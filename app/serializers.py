"""Asset y Column Serializer"""

# Models
from app.models import Asset

# Django REST FRAMEWORK
from rest_framework import serializers

class AssetListSerializer(serializers.Serializer):
    """Asset serializer"""

    name = serializers.CharField()
    column_name = serializers.CharField()
    value = serializers.CharField()

class CreateAssetSerializer(serializers.Serializer):
    """Create asset serializer"""
    name = serializers.ChoiceField(
    choices=[
        'WTG01',
        'WTG02',
        'WTG03',
        'WTG04',
        'WTG05',
        'WTG06',
        'WTG07',
        'WTG08',
        'WTG09',
        'WTG10',
        'WTG11',
        'WTG12',
        'WTG13',
        'WTG14',
        'WTG15',
        'WTG16',
        'WTG17'
    ])
    colum_name = serializers.CharField(max_length=100)
    value = serializers.CharField()

    # Overwrite save instances
    def create(self, data):
        """Create asset"""
        return Asset.objects.create(**data)

