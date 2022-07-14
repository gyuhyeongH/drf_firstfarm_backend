from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article as ArticleModel


# Create your views here.

class ArticleView(APIView):
    def get(self, request):
        locations = ['서울','인천']
        request_front = request.data.get('choice')
        articles = ArticleModel.objects.all()

        if request_front == '추천':
            recommend_articles = recommends(articles, request.user.userprofile.prefer)  # 추천 시스템 함수
            Response(recommend_articles, status=status.HTTP_200_OK)
        elif request_front in locations:
            location_articles = location_article(articles, request_front)  # 지역 별 함수
            return Response(location_articles, status=status.HTTP_200_OK)

        return Response(articles, status=status.HTTP_200_OK)


def recommends(articles, user_prefer):
    recommend_articles =[]
    article_info=[]
    for article in articles:
        article_info.append(article.desc)
    # 코랩에서 user_prefer,articles_info 이용한 코드 작성 밑 테스트 이후 배포할때 추가.
    return recommend_articles


def location_article(articles, request_front):
    location_articles=[]
    for article in articles:
        if request_front in article.location:
            location_articles.append(article)
    return location_articles
