from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Apply as ApplyModel
from article.models import Review as ReviewModel

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = '__all__'

    farm_name = serializers.CharField(required=True, min_length=2)
    title = serializers.CharField(required=True, min_length=4)

    def create(self, validated_data):
        article = ArticleModel.objects.create(
            user=validated_data['user_id'],
            article_category=validated_data['article_category_id'],
            farm_name=validated_data['farm_name'],
            location=validated_data['location'],
            title=validated_data['title'],
            cost=validated_data['cost'],
            requirement=validated_data['requirement'],
            period=validated_data['period'],
            desc=validated_data['desc'],
            img1=validated_data['img1'],
            img2=validated_data['img2'],
            img3=validated_data['img3'],
            # exposure_end_date=validated_data['exposure_end_date'],
            display_article=validated_data['display_article'],
        )
        return article

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            print(key, value)
            setattr(instance, key, value)
        instance.save()
        return instance

class ArticleApplySerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField(read_only=True)

    def get_userinfo(self, obj):
        return {
            "email":obj.user.email,
            "fullname": obj.user.userprofile.fullname if obj.user.userprofile else None,
            "location":obj.user.userprofile.location if obj.user.userprofile else None,
            "prefer": obj.user.userprofile.prefer if obj.user.userprofile else None,
            "gender": obj.user.userprofile.gender if obj.user.userprofile else None,
            "age": obj.user.userprofile.age if obj.user.userprofile else None,
            "introduction": obj.user.userprofile.introduction if obj.user.userprofile else None,
            "phone_number": obj.user.userprofile.phone_number if obj.user.userprofile else None,
            # "img": obj.user.userprofile.img if obj.user.userprofile else None, <- unicodeDecodeError
        }
    class Meta:
        model = ApplyModel
        fields = ["user","article","accept","userinfo"]

    def create(self, validated_data):
        apply = ApplyModel.objects.create(
            user=validated_data['user_id'],
            article = validated_data['article_id']
        )
        return apply

class UserApplySerializer(serializers.ModelSerializer):
    articleinfo = serializers.SerializerMethodField(read_only=True)

    def get_articleinfo(self, obj):
        return {
            "farm_name":obj.article.farm_name if obj.article else None,
            "location": obj.article.location if obj.article else None,
            "title": obj.article.title if obj.article else None,
            "period": obj.article.period if obj.article else None,
            "cost": obj.article.cost if obj.article else None,
            "desc": obj.article.desc if obj.article else None,
        }
    class Meta:
        model = ApplyModel
        fields = ["user","article","accept","articleinfo"]

# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'

    # def create(self, validated_data):
    #     review = ArticleModel.objects.create(
    #         user=validated_data['user'],
    #         article=validated_data['article_id'],
    #         rate=validated_data['rate'],
    #         content=validated_data['content'],
    #         img1=validated_data['img1'],
    #         img2=validated_data['img2'],
    #         img3=validated_data['img3'],
    #     )
    #     return review