from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    UserCategory as UserCategoryModel,
    Rank as UserRankModel
    )


# 유저 관리 페이지 안에서 유저 프로필을 조회할 수 있음(역참조 관계에서만 가능)
class UserProfileInline(admin.StackedInline):
    model = UserProfileModel


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'user_category')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('username', 'email', )
    readonly_fields = ('join_date', )

    fieldsets = (
        ("info", {'fields': ('username', 'password', 'email', 'join_date',)}),
        ('permissions', {'fields':('is_admin', 'is_private', )}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )

    inlines = (
            UserProfileInline,
        )

    # 관리자 계정에서 사용자 계정을 생성하기 위한 필드 설정
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('username', 'email', 'user_category', 'password1', 'password2')}
            ),
    )

    # 권한을 부여할 수도 제거할 수도 특정 조건에 맞는 사용자만 권한을 부여할 수 있음.
    # def has_add_permission(self, request, obj=None): # 추가 권한
    #     return True    

    # def has_delete_permission(self, request, obj=None): # 삭제 권한
    #     return True

    # def has_change_permission(self, request, obj=None): # 수정 권한
    #     return True


# Register your models here.
admin.site.register(UserModel, UserAdmin)
admin.site.register(UserProfileModel)
admin.site.register(UserCategoryModel)
admin.site.register(UserRankModel)