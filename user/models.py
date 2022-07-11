from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime, timedelta

class Preference(models.Model):
    name = models.CharField(verbose_name="선호", max_length=50)

    def __str__(self):
        return self.name


class Rank(models.Model):
    rank_name = models.CharField(verbose_name="사용자 랭크", max_length=50)

    def __str__(self):
        return self.name


class UserCategory(models.Model):
    name = models.CharField(verbose_name="카테고리 이름", max_length=50)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# custom User model
class User(AbstractBaseUser):
    # 회원가입 정보
    username = models.CharField(verbose_name="사용자 계정", max_length=50, unique=True)
    password = models.CharField(verbose_name="사용자 비밀번호", max_length=128)
    email = models.EmailField(verbose_name="사용자 이메일", max_length=254)
    join_date = models.DateTimeField(verbose_name="가입일", auto_now_add=True)

    # user category
    user_category = models.ForeignKey(UserCategory, verbose_name="카테고리",on_delete=models.SET_NULL,null=True)

    is_private = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin


# 가입자 상세 정보
class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="사용자", on_delete=models.CASCADE)
    prefer = models.ForeignKey(Preference, verbose_name="사용자 선호도",on_delete=models.SET_NULL,null=True)
    rank = models.ForeignKey(Rank, verbose_name="랭크",on_delete=models.SET_NULL,null=True)

    fullname = models.CharField(verbose_name="이름",max_length=128)
    location = models.CharField(verbose_name="지역",max_length=128)

    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
        )

    gender = models.CharField(verbose_name="성별", max_length=1, choices=GENDERS)

    age = models.IntegerField(verbose_name="나이")
    introduction = models.TextField(verbose_name="자기소개", null=True, blank=True)
    birthday = models.DateField(verbose_name="생일")
    img = models.ImageField(verbose_name="프로필이미지", upload_to=user,default=datetime
                             .now(),null=True)

    def __str__(self):
        return f"{self.user.username} 님의 프로필입니다."