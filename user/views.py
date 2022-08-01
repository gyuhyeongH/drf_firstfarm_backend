from ast import literal_eval
from cmath import polar
import json
from django.http import QueryDict

from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer, UserSiginUpSerializer, UserSiginPutSerializer
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
        data = request.data.copy()
        print("1번")
        print(data)

        try:
            if data['username'] == 'test1234':
                query_dict_data = QueryDict('', mutable=True)
                query_dict_data.update(data)
                print("1-1번")
                print(query_dict_data)

                data = query_dict_data
        except:
            pass

        for i in data:
            if data[i] == "":
                return Response("회원정보가 없습니다.", status=status.HTTP_400_BAD_REQUEST)
                
        profile_data = data.pop('userprofile')[0]
        print("2번")
        print(profile_data)
        img_data = data.pop('img')[0]
        print("3번")
        print(img_data)

        try:
            if data['username'] != 'test':
                profile_data = literal_eval(profile_data)
                print("4번")
                print(profile_data)
        except:
            pass

        if img_data != "undefined":
            profile_data['img'] = img_data

        print("5번")
        print(img_data)

        # profile_data['img'] = img_data

        data['userprofile'] = profile_data
        print("6번")
        print(data)

        serializer = UserSiginUpSerializer(data=data.dict(), context={"request" : request})
        print("7번")
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # return Response({"message": f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 수정
    def put(self, request, obj_id):
        # user = request.user
        # print(user)

        try:
            user = UserModel.objects.get(pk=obj_id)
            print(user)
        except user.DoesNotExist:
            return Response(status=404)

        data = request.data.copy()
        print("1번")
        print(data)

        profile_data = data.pop('userprofile')[0]
        print("2번")
        print(profile_data)

        # profile_data = json.dumps(profile_data)
        # print(profile_data)
        
        img_data = data.pop('img')[0]
        print("3번")
        print(img_data)

        profile_data = literal_eval(profile_data)
        profile_data['img'] = img_data

        print("4번")
        print(profile_data)

        print("5번")
        print(data)

        data['userprofile'] = profile_data
        print("5-1번")
        print(data)
        print(data.dict())

        # json_trans_data = json.loads(json.dumps(data))
        # print(json_trans_data)

        # username 수정 불가
        data.pop("username", "")
        user_serializer = UserSiginPutSerializer(user, data=data.dict(), context={"request" : request})
        # print(user_serializer)

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
            return Response("회원 탈퇴 완료", status=status.HTTP_200_OK)


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