
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, UserDetailSerializer
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from articles.serializers import ArticleSerializer, CommentSerializer
from articles.models import Article,Comment
class UserSignup(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self,request):
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.filter(username=username).first()
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response=Response(
                {
                    'user' : UserSerializer(user).data,
                    "jwt_token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token
                    },
                },
            status=status.HTTP_200_OK)
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response({"message":"로그인 실패입니다."},status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    def put(self,request, username):
        user=get_object_or_404(get_user_model(),username=username)
        if "username" in request.data:
            return Response({"message":"username은 수정할 수 없습니다."},status=status.HTTP_400_BAD_REQUEST)
        if request.user != user:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
        serializer=UserDetailSerializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,username):
        user=get_object_or_404(get_user_model(),username=username)
        if request.user != user:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
        else:
            password = request.data.get("password")
            if not password:
                return Response({"error": "password is required"}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.check_password(password):
                return Response({"error": "password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            request.user.delete()
            return Response({"message": "user is deleted"}, status=status.HTTP_204_NO_CONTENT)

class WriteArticleAPIView(APIView):
    def get(self, request,username):
        user=get_object_or_404(get_user_model(),username=username)
        articles=Article.objects.all().filter(author=user.pk)
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

class WriteCommentAPIView(APIView):
    def get(self, request,username):
        user=get_object_or_404(get_user_model(),username=username)
        comments=Comment.objects.all().filter(author=user.pk)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)

class FavoriteArticleAPIView(APIView):
    def get(self, request,username):
        user=get_object_or_404(get_user_model(),username=username)
        articles=Article.objects.all().filter(likes=user.pk)
        serializer = ArticleSerializer(articles,many=True)
        return Response(serializer.data)

class FavoriteCommentAPIView(APIView):
    def get(self, request,username):
        user=get_object_or_404(get_user_model(),username=username)
        comments=Comment.objects.all().filter(favorite=user.pk)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)

