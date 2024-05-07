from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.d
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(get_user_model())