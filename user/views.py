from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .models import UserCategory as UserCategoryModel
from .models import Rank as RankModel


class UserView(APIView):
    # permission_classes = [permissions.AllowAny]

    # 사용자 정보 조회
    def get(self, request):
        return Response({"message": "get method"})

    # 회원가입
    def post(self, request):
        return Response({"message": "post method!!"})

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})

    # 회원 탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})


class UserAPIView(APIView):
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "login success!!"})

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})