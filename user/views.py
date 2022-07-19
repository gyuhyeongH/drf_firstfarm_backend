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
        user_serializer = UserSerializer(user).data

        return Response(user_serializer, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        serializer = UserSiginUpSerializer(data=request.data, partial=True, context={"request" : request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data="INFO_INVALID", status=status.HTTP_400_BAD_REQUEST)

    # 수정
    def put(self, request, obj_id):
        user = request.user

        # username 수정 불가
        request.data.pop("username", "")
        user_serializer = UserSiginUpSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response({"message": f'${user_serializer.errors}'}, 400)

    # 회원탈퇴 = 삭제
    def delete(self, request, obj_id):
        if obj_id is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = obj_id
            user_object = UserModel.objects.get(id=user_id)
            user_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)


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