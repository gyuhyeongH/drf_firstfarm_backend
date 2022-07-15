from rest_framework import serializers
from user.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    UserCategory as UserCategoryModel,
    Rank as UserRankModel
    )


class UserCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCategoryModel
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):

    user_category = UserCategorySerializer()

    class Meta:
        model = UserModel
        fields = [ 'id', 'username', 'email', 'join_date', 'user_category' ]


class UserSiginUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfileModel
        fields = [ "id" ]


class UserSiginUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [ "username", "password", "email", "user_category", "join_date" ]

    username = serializers.CharField(required=True, min_length=4)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=4)

    def create(self, validated_data):

        user_category_id = validated_data['user_category']

        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_category = user_category_id
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user


    def update(self, *args, **kwargs):
        user = super().create(**args, **kwargs)
        p = user.password

        user.set_password(p)
        user.save()
        return user