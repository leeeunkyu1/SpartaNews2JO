from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path('<int:article_pk>/comments/', views.CommentsView.as_view(), name='comments'),
    path("<int:article_pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
]
