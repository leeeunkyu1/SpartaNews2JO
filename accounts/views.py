from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
# from articles.models import Article, Comment

class UserDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# class WriteArticleAPIView(APIView):
#     def get(self, request,username):
#         articles=get_object_or_404(Article,author=username)
#         serializer = UserSerializer(articles)
#         return Response(serializer.data)

# class WriteCommentAPIView(APIView):
#     def get(self, request,username):
#         comments=get_object_or_404(Comment,author=username)
#         serializer = UserSerializer(comments)
#         return Response(serializer.data)

# class FavoriteArticleAPIView(APIView):
#     def get(self, request,username):
#         articles=get_object_or_404(Article,favorite=username)
#         serializer = UserSerializer(articles)
#         return Response(serializer.data)

# class FavoriteCommentAPIView(APIView):
#     def get(self, request,username):
#         comments=get_object_or_404(Comment,favorite=username)
#         serializer = UserSerializer(comments)
#         return Response(serializer.data)