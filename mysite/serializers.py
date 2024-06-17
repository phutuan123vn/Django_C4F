from pprint import pprint
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    conf_pass = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username','id','password','conf_pass')

    def validate(self, data):
        # print(data)
        if data['password'] != data['conf_pass']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def create(self):
        user = User(
            username=self.validated_data['username'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

