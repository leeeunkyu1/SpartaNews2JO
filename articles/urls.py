from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path('<int:article_pk>/', views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path('<int:article_pk>/comments/', views.CommentView.as_view(), name='comment'),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<int:article_pk>/like/', views.ArticleLikeAPIView.as_view(), name='article_like'),
]
