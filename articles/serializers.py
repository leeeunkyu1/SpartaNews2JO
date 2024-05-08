from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = "__all__"
        
        
class ArticleDetailSerializer(ArticleSerializer):
    pass

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)
    
    
    class Meta:
        model = Comment
        fields = "__all__"

