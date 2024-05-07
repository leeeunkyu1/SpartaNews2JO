from urllib import request
from rest_framework import serializers
from .models import Article
from django.contrib.auth import get_user_model

user = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    user = request.user(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"



        
        
        
        
class ArticleDetailSerializer(ArticleSerializer):
    pass        


