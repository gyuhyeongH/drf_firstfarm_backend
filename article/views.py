from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article as ArticleModel
from article.serializers import ArticleSerializer, ArticleCreateSerializer



# Create your views here.
class ArticleDetailView(APIView):

    def get(self, request):
        article = ArticleModel.objects.all()
        serializer = ArticleSerializer(article, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글이 작성되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)