from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            #provide django, password will be hashing!
            instance.set_password(password)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "intro",
            'password',
            'date_joined',
            'write_articles',
            'write_comments',
            'favorite_articles',
            'favorite_comments',
        ]
        read_only_fields =[
            'username',
            'date_joined',
            'write_articles',
            'write_comments',
            'favorite_articles',
            'favorite_comments',
        ]
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("password")
        return ret

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if "email" in attrs:
            if get_user_model().objects.filter(email=attrs["email"]).exists():
                raise serializers.ValidationError("email exists")

        if "username" in attrs:
            if get_user_model().objects.filter(username=attrs["username"]).exists():
                raise serializers.ValidationError("username exists")

        return attrs
    
    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        for key,value in validated_data.items():
            setattr(instance,key,value)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance

