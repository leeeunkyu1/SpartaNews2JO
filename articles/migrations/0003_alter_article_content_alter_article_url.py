# Generated by Django 4.2.11 on 2024-05-09 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, verbose_name='내용'),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(blank=True, verbose_name='URL'),
        ),
    ]
