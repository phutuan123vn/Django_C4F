from os import read
from rest_framework import serializers
from chatapp import models


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Code
        fields = "__all__"
        
    def create(self, validated_data):
        return models.Code.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.code = validated_data.get('code',instance.code)
        instance.save()
        return instance
    

class ChatRoomSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = models.Room
        fields = ['name','group','creator','id']
        read_only_fields = ['group']
        
    def create(self, validated_data):
        return models.Room.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.save()
        return instance
    
class MessageSerializer(serializers.ModelSerializer):
    # user__username = serializers.ReadOnlyField(source='user.username')
    username = serializers.CharField(source='user__username')
    class Meta:
        model = models.Message
        fields = ['value','date','id','username']
        # read_only_fields = ['room']
        
    def create(self, validated_data):
        return models.Message.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.value = validated_data.get('value',instance.value)
        instance.save()
        return instance