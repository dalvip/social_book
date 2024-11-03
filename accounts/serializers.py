from rest_framework import serializers
from .models import UploadFile  # Adjust if needed

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'  # Or list specific fields
