from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("<str:username>/", views.UserDetailAPIView.as_view(), name="profile"),
    path("<str:username>/articles/", views.WriteArticleAPIView.as_view(), name="write_article"),
    path("<str:username>/comments/", views.WriteCommentAPIView.as_view(), name="write_comment"),
    path("<str:username>/articles-favorite/", views.FavoriteArticleAPIView.as_view(), name="favorite_article"),
    path("<str:username>/comments-favorite/", views.FavoriteCommentAPIView.as_view(), name="favorite_comment"),
]
