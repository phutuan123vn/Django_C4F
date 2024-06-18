from pprint import pprint
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get('username','')
        password = data.get('password','')
        if username and password:
            user = User.objects.filter(username=username).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError({"password":"Incorrect Password"})
            else:
                raise serializers.ValidationError({"username":"User not found"})
        else:
            raise serializers.ValidationError({"username":"This field is required"})
        return data

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
    
    def create(self,validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

