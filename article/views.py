from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article as ArticleModel
from article.serializers import ArticleSerializer
from article.serializers import ArticleApplySerializer
import json

class ArticleView(APIView):
    def get(self, request):
        locations = ["서울", "경기", "인천", "강원", "대전", "세종", "충남", "충북",
                     "부산", "울산", "경남", "경북", "대구", "광주", "전남", "전북", "제주", " "]
        request_front = request.data.get('choice')
        print(request.data.get("choice"))

        articles = ArticleModel.objects.all()

        if request_front == '추천':
            recommend_articles = recommends(articles, request.user.userprofile.prefer)  # 추천 시스템 함수
            recommend_articles_serializer = ArticleSerializer(recommend_articles, many=True).data
            Response(recommend_articles_serializer, status=status.HTTP_200_OK)

        elif request_front in locations:
            location_articles = location_article(articles, request_front)  # 지역 별 함수
            location_articles_serializer = ArticleSerializer(location_articles, many=True).data
            return Response(location_articles_serializer, status=status.HTTP_200_OK)

        articles_serializer = ArticleSerializer(articles, many=True).data
        return Response(articles_serializer, status=status.HTTP_200_OK)


def recommends(articles, user_prefer):
    recommend_articles = []
    article_info = []
    for article in articles:
        article_info.append(article.desc)
    # 코랩에서 user_prefer,articles_info 이용한 코드 작성 밑 테스트 이후 배포할때 추가.
    return recommend_articles


def location_article(articles, request_front):
    location_articles = []
    for article in articles:
        if request_front in article.location:
            location_articles.append(article)
    return location_articles


class ArticleDetailView(APIView):

    def get(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        # authentication_classes = [JWTAuthentication]

        serializer = ArticleSerializer(article, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글이 작성되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, article_id):
        user = request.user
        article = ArticleModel.objects.get(id=article_id)
        serializer = ArticleSerializer(article, data=request.data, partial=True)

        # if user.is_anonymous:
        #     return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, article_id):
    #     user = request.user
    #     article = ArticleModel.objects.get(id=article_id)
    #     if user == article.user_id:
    #         return Response({"message": "게시글 마감 성공."}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"message": "게시글 마감 실패."}, status=status.HTTP_400_BAD_REQUEST)


class ArticleApplyView(APIView):

    def post(self, request, article_id):
        # user = request.user
        # article = ArticleModel.objects.get(id=article_id)
        serializer = ArticleApplySerializer(data=request.data)

        # if user.is_anonymous:
        #     return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "신청이 완료되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
