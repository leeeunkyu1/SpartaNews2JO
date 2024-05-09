
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # access token을 쿠키에서 삭제
        response = Response({"detail":"로그아웃 완료"},status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        # refresh token을 블랙리스트에 추가
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                response.delete_cookie('refresh_token')
            except Exception as e:
                response = Response({"message":"로그아웃에 실패했습니다."},status=status.HTTP_400_BAD_REQUEST)
            return response
        return Response({"message":"이미 로그아웃했습니다"},status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    def put(self,request, username):
        user=get_object_or_404(get_user_model(),username=username)
        if "username" in request.data:
            return Response({"message":"username은 수정할 수 없습니다."},status=status.HTTP_400_BAD_REQUEST)
        if "password" in request.data:
            if request.data["password"]!=request.data["password2"]:
                return Response({"message":"비밀번호가 일치하지 않습니다."},status=status.HTTP_400_BAD_REQUEST)
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
                return Response({"error": "비밀번호를 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.check_password(password):
                return Response({"error": "입력한 비밀번호가 틀립니다"}, status=status.HTTP_400_BAD_REQUEST)

            request.user.delete()
            return Response({"message": "회원탈퇴가 완료했습니다"}, status=status.HTTP_204_NO_CONTENT)

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

