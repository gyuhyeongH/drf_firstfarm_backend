from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article


# Create your views here.

class ArticleView(APIView):
    def get(self, request):
        locations = []
        request_front = request.data.get()
        articles = Article.objects.all()

        if request_front == '추천':
            recommend_articles = recommends(articles, request.user.userprofile.prefer)  # 추천 시스템 함수
            Response(recommend_articles, status=status.HTTP_200_OK)
        elif request_front in locations:
            location_articles = location_article(articles, request_front)  # 지역 별 함수
            return Response(location_articles, status=status.HTTP_200_OK)
        else:
            return Response(articles, status=status.HTTP_200_OK)


def recommends(articles, user_prefer):
    recommend_articles =[]
    # 여기에서 어떤 과정이 있고 거기에 유저의 성향과 위치만 넣는 그런 방식이 되어야 할듯.
    return recommend_articles


def location_article(articles, request_front):
    location_articles=[]
    for article in articles:
        if request_front in article.location:
            location_articles.append(article)
    return location_articles
