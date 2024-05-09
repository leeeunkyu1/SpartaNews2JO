
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, UserDetailSerializer
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from articles.serializers import ArticleSerializer
from articles.models import Article
class UserSignup(APIView):
    def post(self, request):
        data=request.data
        email = data.get("email")
        username = data.get("username")
        errors = {}
        if not email or not username:
            errors["error"] = "email or username is required"
        else:
            if get_user_model().objects.filter(email=email).exists():
                errors["email"] = "email already exists"
            if get_user_model().objects.filter(username=username).exists():
                errors["username"] = "username already exists"

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=data.get("password"),
            intro = data.get("intro"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name")
        )
        return Response({
            "id":user.id,
            "username":user.username,
            "email":user.email,
            "intro":user.intro
        },
        status=status.HTTP_201_CREATED)

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

