# Generated by Django 4.2.11 on 2024-05-07 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='제목')),
                ('url', models.URLField(verbose_name='URL')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='업데이트 날짜')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('likes', models.ManyToManyField(related_name='article_likes', to=settings.AUTH_USER_MODEL, verbose_name='좋아요')),
            ],
            options={
                'verbose_name': '뉴스',
                'verbose_name_plural': '뉴스모음',
            },
        ),
    ]
