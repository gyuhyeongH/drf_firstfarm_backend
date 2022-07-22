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
    display_article = serializers.BooleanField(default=True)

    def create(self, validated_data):
        article = ArticleModel.objects.create(
            user=validated_data['user'],
            article_category=validated_data['article_category'],
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
            "fullname": obj.user.userprofile.fullname,
            "location":obj.user.userprofile.location,
            "prefer": obj.user.userprofile.prefer,
            "gender": obj.user.userprofile.gender,
            "age": obj.user.userprofile.age,
            "introduction": obj.user.userprofile.introduction,
            "phone_number": obj.user.userprofile.phone_number,
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
            "farm_name":obj.article.farm_name,
            "location": obj.article.location ,
            "title": obj.article.title,
            "period": obj.article.period,
            "cost": obj.article.cost,
            "desc": obj.article.desc,
        }
    class Meta:
        model = ApplyModel
        fields = ["user","article","accept","articleinfo"]

# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'
