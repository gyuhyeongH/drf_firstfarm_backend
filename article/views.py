from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article as ArticleModel
from article.serializers import ArticleSerializer


# Create your views here.
class ArticleDetailView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        article = ArticleModel.objects.all()
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

        if user.is_anonymous:
            return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)

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
