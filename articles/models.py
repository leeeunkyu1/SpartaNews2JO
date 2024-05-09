from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Article(models.Model):
    
    Category = (
    ('news', '뉴스'),
    ('review', '리뷰'),
    ('interview', '인터뷰'),
    ('opinion', '칼럼'),
    )
    
    type = models.CharField(max_length=20, choices=Category, verbose_name="뉴스 유형")
    title = models.CharField(max_length=255, verbose_name="제목")
    url = models.URLField(max_length=200, verbose_name="URL")
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트 날짜")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="article_likes", verbose_name="좋아요")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '뉴스'
        verbose_name_plural = '뉴스모음'
# Create your models here.d
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comment_favorites", blank="True")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
