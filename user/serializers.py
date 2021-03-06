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


class UserProfileRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRankModel
        fields = [ "id", "rank_name" ]


class UserProfileSerializer(serializers.ModelSerializer):

    rank = UserProfileRankSerializer(required=False)
    
    class Meta:
        model = UserProfileModel
        fields = [ 'prefer', 'fullname', 'location', 'gender', 'age', 'introduction', 'birthday', 'phone_number', 'rank']


class UserSerializer(serializers.ModelSerializer):

    user_category = UserCategorySerializer()
    userprofile = UserProfileSerializer()

    class Meta:
        model = UserModel
        fields = [ 'id', 'username', 'email', 'join_date', 'user_category', 'userprofile' ]

        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            }


class UserSiginUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [ "username", "password", "email", "user_category", "join_date", "userprofile" ]

        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            "password": {'write_only': True}, # default : False
            "email": {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            }

    # username = serializers.CharField(required=True, min_length=4)
    # email = serializers.EmailField(required=True)
    # password = serializers.CharField(required=True, min_length=4)

    userprofile = UserProfileSerializer()

    def create(self, validated_data):
        # User object 생성
        user_category_id = validated_data['user_category']
        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_category = user_category_id,
        )
        user.set_password(validated_data['password'])
        user.save()

        # UserProfile object 생성
        user_profile = validated_data.pop("userprofile")
        # 첫 회원가입시 id = 1 : name = 씨앗 default
        user_profile = UserProfileModel.objects.create(user=user, rank_id=1, **user_profile)

        return user


    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        user_profile = validated_data.pop("userprofile")
        
        # 유저 필수 정보 수정
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save()

        # 프로필 정보 수정
        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value)

        user_profile_object.save()

        return instance