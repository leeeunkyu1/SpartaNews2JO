from django.shortcuts import get_object_or_404, render
from articles.serializers import ArticleSerializer, CommentSerializer
from .models import Article
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Article, Comment
from django.conf import settings


class ArticleListAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentsView(APIView):
    # 댓글조회 나중에 article 조회로 옮길 것
    def get(self,request, article_pk):
        pass

    def post(self, request, article_pk):
        content = request.data.get('content')
        article = get_object_or_404(Article, pk=article_pk)
        comment = Comment.objects.create(
            content=content,
            author=request.user,
            article=article,
        )
        serializer = CommentSerializer(comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 댓글 작성
    # def post(self, request, article_pk):
    #     print('\n\n'+request.user)
    #     content = request.data['content']
    #     author = request.user
    #     article = get_object_or_404(Article, pk=article_pk)
    #     comment = Comment.objects.create(
    #         content = content, author = author, article = article,
    #     )
    #     serializer = CommentSerializer(comment)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    # 댓글 수정
    def put(self, request, article_pk):
        pass
    # 댓글 삭제
    def delete(self, request, article_pk):
        pass


