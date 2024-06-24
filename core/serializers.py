# serializers.py
from rest_framework import serializers
from .models import CondicionesCultivo

class CondicionesCultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionesCultivo
        fields = '__all__'
