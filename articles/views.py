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
    def get(self, request):
        category = request.query_params.get('category')
        if category:
            articles = Article.objects.filter(type=category)
        else:
            articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "로그인이 필요합니다."}, status=400)
        
class ArticleDetailAPIView(APIView):
    def get_object(self, article_pk):
        return get_object_or_404(Article, pk=article_pk)

    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, article_pk):
        article = self.get_object(article_pk)
        if request.user.is_authenticated:
            if request.user==article.author:
                serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.data)
            return Response({"message":"권한이 없습니다"})
        else:
            return Response({"error": "로그인이 필요합니다."}, status=400)
    
    def delete(self, request, article_pk):
        article = self.get_object(article_pk)
        if request.user.is_authenticated:
            if request.user == article.author:
                article.delete()
                data = {"message": "게시글이 삭제되었습니다"}
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message":"권한이 없습니다"})
        else:
            return Response({"error": "로그인이 필요합니다."}, status=400)
    
class ArticleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        article.likes.add(request.user)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    def delete(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        article.likes.remove(request.user)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
class CommentView(APIView):
    # 댓글 조회 나중에 article 조회랑 합칠 것
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 작성
    def post(self, request, article_pk):
        if request.user.is_authenticated:
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
        else:
            return Response({"error": "로그인이 필요합니다."}, status=400)

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    # 댓글 수정
    def put(self, request, article_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.author:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "권한이 없습니다"}, status=400)
    # 댓글 삭제
    def delete(self, request, article_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            return Response({"mssege":"댓글이 삭제되었습니다"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "권한이 없습니다"}, status=400)

class CommentFavoriteView(APIView):
    def post(self, request, article_pk, comment_pk):
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if comment.favorite.filter(pk=request.user.pk).exists():
                comment.favorite.remove(request.user)
            else:
                comment.favorite.add(request.user)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "로그인이 필요합니다."}, status=400)

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
