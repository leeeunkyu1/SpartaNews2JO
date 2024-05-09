from django.shortcuts import get_object_or_404, render
from articles.serializers import ArticleDetailSerializer, ArticleSerializer, CommentSerializer
from .models import Article
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from .models import Article, Comment
from django.conf import settings
from rest_framework import generics
from django.db.models import Q

class ArticleListAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.query_params.get('category')
        if category:
            articles = Article.objects.filter(type=category)
        else:
            articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def delete(self, request, article_pk):
        article = self.get_object(article_pk)
        article.delete()
        data = {"pk": f"{article_pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)
    
    
class ArticleLikeAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        article.likes.add(request.user)
        return Response({"message": "Liked"}, status=status.HTTP_200_OK)
    def delete(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        article.likes.remove(request.user)
        return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
    
    
    
    
    
    
class CommentView(APIView):
    # 댓글 조회 나중에 article 조회랑 합칠 것
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 작성
    def post(self, request, article_pk):
        content = request.data.get('content')
        article = get_object_or_404(Article, pk=article_pk)
        comment = Comment.objects.create(
            content=content,
            author=request.user,
            article=article,
        )
        serializer = CommentSerializer(comment, data=request.data)
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

class CommentDetailView(APIView):
    # 댓글 수정
    def put(self, request, article_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.author:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You do not have permission to edit this comment."}, status=400)
    # 댓글 삭제
    def delete(self, request, article_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to delete this comment."}, status=400)


class SearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        query_params = self.request.query_params
        title = query_params.get("title")
        content = query_params.get("content")
        author = query_params.get("author")

        q = Q()
        if title:
            q |= Q(title__icontains=title)
        if content:
            q |= Q(content__icontains=content)
        if author:
            q |= Q(author__username=author)

        return Article.objects.filter(q)