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
        # print(validated_data)
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
            display_article=True,
        )

        return article

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            print(key, value)
            setattr(instance, key, value)
        instance.save()
        return instance


class ArticleApplySerializer(serializers.ModelSerializer):


    class Meta:
        model = ApplyModel
        fields = ["user", "article", "accept"]

    def create(self, validated_data):
        print(validated_data)
        apply = ApplyModel.objects.create(
            user=validated_data['user'],
            article=validated_data['article'],
            accept=False
        )
        return apply


class UserApplySerializer(serializers.ModelSerializer):
    articleinfo = serializers.SerializerMethodField(read_only=True)

    def get_articleinfo(self, obj):
        return {
            "farm_name": obj.article.farm_name,
            "location": obj.article.location,
            "title": obj.article.title,
            "period": obj.article.period,
            "cost": obj.article.cost,
            "desc": obj.article.desc,
        }

    class Meta:
        model = ApplyModel
        fields = ["user", "article", "accept", "articleinfo"]


# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'
