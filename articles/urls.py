from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('int:article_pk/comments', views.CommentsView.as_view(), name='comments')
]