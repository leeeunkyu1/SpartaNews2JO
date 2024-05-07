from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("<str:username>/", views.UserDetailAPIView.as_view(), name="profile"),
    # path("<str:username>/articles/", views.WriteArticleAPIView.as_view(), name="write_article"),
    # path("<str:username>/comments/", views.WriteCommentAPIView.as_view(), name="write_comment"),
    # path("<str:username>/articles-favorite/", views.FavoriteArticleAPIView.as_view(), name="favorite_article"),
    # path("<str:username>/comments-favorite/", views.FavoriteCommentAPIView.as_view(), name="favorite_comment"),
]
