from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import UserProfile

class FirstFarmTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 생성된 토큰 가져오기
        token = super().get_token(user)

        # 사용자 지정 클레임 설정하기
        userprofile = UserProfile.objects.get(user=user)
        token['fullname'] = userprofile.fullname

        return token
