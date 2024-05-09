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
        read_only_fields = ("likes",)
        
class ArticleDetailSerializer(ArticleSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comments_cnt = serializers.IntegerField(source="comment_set.count", read_only=True)


