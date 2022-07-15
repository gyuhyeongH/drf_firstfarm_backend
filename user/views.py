from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import  status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer, UserSiginUpSerializer, UserCategorySerializer
from user.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    UserCategory as UserCategoryModel,
    Rank as UserRankModel
    )

# user/
class UserView(APIView):
    permission_classes = [permissions.AllowAny]       # 누구나 view 접근 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인된 사용자만 view 접근 가능
    
    # 사용자 정보 조회
    def get(self, request):
        
        user = request.user
        user_serializer = UserSiginUpSerializer(user).data

        return Response(user_serializer, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        serializer = UserSiginUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, 400)

    # 수정
    def put(self, request):
        return Response({'message': 'put method!!'})

    # 삭제
    def delete(self, request):
        return Response({'message': 'delete method!!'})


# 로그아웃 user/api/logout
class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)