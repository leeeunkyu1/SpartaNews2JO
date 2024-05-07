from rest_framework import serializers
from .models import Article
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(ArticleSerializer):
    pass        


