from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article", "author","favorite",)
    def to_representation(self, instance):
        ret = super(). to_representation(instance)
        ret.pop("article")
        return ret


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("Like", "favorite",)
        
class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.IntegerField(source="comments.count", read_only=True)



