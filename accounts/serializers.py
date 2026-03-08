from rest_framework import serializers
from .models import User, Student, Teacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #define exactly which fields are visible in the API
        fields = ['id', 'username', 'email', 'real_name', 'is_student', 'is_teacher', 'status_update']