
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserDetailSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from articles.serializers import ArticleSerializer
from articles.models import Article
class UserSignup(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = response.data.get('user')
            refresh = RefreshToken.for_user(user)
            response.data['refresh'] = str(refresh)
            response.data['access'] = str(refresh.access_token)
        return response


class UserDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

class WriteArticleAPIView(APIView):
    def get(self, request,username):
        user=get_object_or_404(get_user_model(),username=username)
        articles=Article.objects.all().filter(author=user.pk)
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

# class WriteCommentAPIView(APIView):
#     def get(self, request,username):
#         comments=get_object_or_404(Comment,author=username)
#         serializer = UserSerializer(comments)
#         return Response(serializer.data)

class FavoriteArticleAPIView(APIView):
    def get(self, request,username):
        user=get_object_or_404(get_user_model(),username=username)
        articles=Article.objects.all().filter(likes=user.pk)
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

# class FavoriteCommentAPIView(APIView):
#     def get(self, request,username):
#         comments=get_object_or_404(Comment,favorite=username)
#         serializer = UserSerializer(comments)
#         return Response(serializer.data)

