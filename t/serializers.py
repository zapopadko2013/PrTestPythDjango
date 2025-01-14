from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone','password','status','name')
class UserPhoneNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone','name')        
