from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class ArticleCategory(models.Model):
    name = models.CharField("카테고리", max_length=30)

    def __str__(self):
        return self.name

class Article(models.Model):
    # user_id = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    # prefer_id = models.ForeignKey('user.Preference', verbose_name="취향", on_delete=models.SET_NULL, null=True)
    article_category_id = models.ForeignKey(ArticleCategory, verbose_name="카테고리", on_delete=models.SET_NULL, null=True)
    name = models.CharField("제목", max_length=30)
    location = models.CharField("위치", max_length=128)
    desc = models.TextField("상세 내용")
    imgs = models.ImageField("이미지")
    display_article = models.BooleanField("게시글 노출", default=True)
    exposure_end_date = models.DateTimeField("노출 종료 시간", default=datetime.now() + timedelta(days=7))
    created_at = models.DateTimeField("만든 날", auto_now_add=True)
    updated_at = models.DateTimeField("업데이트 한 날", auto_now=True)

    def __str__(self):
        return self.name

class Apply(models.Model):
    # user_id = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    article_id = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.SET_NULL, null=True)
