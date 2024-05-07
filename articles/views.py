from django.shortcuts import get_object_or_404, render
from articles.serializers import ArticleDetailSerializer, ArticleSerializer
from .models import Article
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Article

# Create your views here.


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
        
        
        
class ArticleDetailAPIView(APIView):
    
    
    # permission_classes = [IsAuthenticated]
		
    def get_object(self, article_pk):
        return get_object_or_404(Article, pk=article_pk)

    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)        