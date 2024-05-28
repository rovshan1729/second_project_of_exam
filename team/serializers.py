from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 
            'name', 
            'last_name', 
            'phone', 
            'image_url',
            'created_at',
            'updated_at',
            )
