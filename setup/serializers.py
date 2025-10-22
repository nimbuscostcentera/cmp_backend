from rest_framework import serializers
from .models import SetupInfo, ProcessWiseControl


class SetupInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupInfo
        fields = '__all__'


class ProcessWiseControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessWiseControl
        fields = '__all__'
