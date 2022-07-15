from django.db import models
from datetime import datetime, timedelta


# Create your models here.
class ArticleCategory(models.Model):
    name = models.CharField("카테고리", max_length=30)

    def __str__(self):
        return self.name


class Article(models.Model):
    user_id = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE, null=True)
    article_category_id = models.ForeignKey(ArticleCategory, verbose_name="카테고리", on_delete=models.SET_NULL, null=True)
    farm_name = models.CharField("농장 이름", max_length=16)
    location = models.CharField("위치", max_length=128)
    title = models.CharField("제목", max_length=30)
    cost = models.CharField("금액", max_length=16)
    requirement = models.CharField("모집 요건", max_length=256)
    period = models.CharField("참여 기간", max_length=256)
    desc = models.TextField("세부 내용")
    img1 = models.ImageField(verbose_name="업로드 이미지1", upload_to='img/', null=True)
    img2 = models.ImageField(verbose_name="업로드 이미지2", upload_to='img/', null=True)
    img3 = models.ImageField(verbose_name="업로드 이미지3", upload_to='img/', null=True)
    display_article = models.BooleanField("게시글 노출", default=True)
    exposure_end_date = models.DateTimeField("모집 기간", default=datetime.now() + timedelta(days=7))
    created_at = models.DateTimeField("만든 날", auto_now_add=True)
    updated_at = models.DateTimeField("업데이트 한 날", auto_now=True)
    # img1 = models.ImageField(verbose_name="업로드 이미지1", upload_to='img/', default=datetime
    #                          .now() + timedelta(seconds=1), blank=True)
    # img2 = models.ImageField(verbose_name="업로드 이미지2", upload_to='img/', default=datetime
    #                          .now() + timedelta(seconds=2), blank=True)
    # img3 = models.ImageField(verbose_name="업로드 이미지3", upload_to='img/', default=datetime
    #                          .now() + timedelta(seconds=3), blank=True)

    def __str__(self):
        return self.title


class Apply(models.Model):
    user_id = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    article_id = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.SET_NULL, null=True)
    accept = models.BooleanField("신청 수락", default=False)

    def __str__(self):
        return f"{self.user_id} 님의 [{self.article_id}] 게시글 신청 입니다."

class Review(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    rate = models.IntegerField('평가점수', default=0)
    img1 = models.ImageField(verbose_name="업로드 이미지1", upload_to=user, default=datetime
                             .now(), null=True)
    img2 = models.ImageField(verbose_name="업로드이미지2", upload_to=user, default=datetime
                             .now(), null=True)
    img3 = models.ImageField(verbose_name="업로드이미지3", upload_to=user, default=datetime
                             .now(), null=True)
    content = models.TextField("댓글")
    created_at = models.DateTimeField("댓글 작성 일", auto_now_add=True)
    updated_at = models.DateTimeField("업데이트 일", auto_now=True)

    def __str__(self):
        return f'id [ {self.id} ] {self.article.title} : {self.content} / {self.user.username}님이 작성한 리뷰'
