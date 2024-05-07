from django.db import models
from django.contrib.auth.models import AbstractUser
<<<<<<< HEAD

LOCAL_HOST="http://127.0.0.1:8000/"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    intro=models.TextField(blank=True)
    
    @property
    def write_articles(self):
        return f"{LOCAL_HOST}/accounts/{self.username}/articles/"
    
    @property
    def write_comments(self):
        return f"{LOCAL_HOST}/accounts/{self.username}/comments/"
    
    @property
    def favorite_articles(self):
        return f"{LOCAL_HOST}/accounts/{self.username}/articles-favorite/"
    
    @property
    def favorite_comments(self):
        return f"{LOCAL_HOST}/accounts/{self.username}/comments-favorite/"
=======
# Create your models here.
class User(AbstractUser):
    pass
>>>>>>> develop
