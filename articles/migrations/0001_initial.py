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
                ('type', models.CharField(choices=[('news', '뉴스'), ('review', '리뷰'), ('interview', '인터뷰'), ('opinion', '칼럼')], max_length=20, verbose_name='뉴스 유형')),
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
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank='True', related_name='comment_favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
