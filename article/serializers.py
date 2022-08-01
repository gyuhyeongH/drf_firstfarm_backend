from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Apply as ApplyModel
from article.models import Review as ReviewModel


class ArticleSerializer(serializers.ModelSerializer):
    # article_review = serializers.SerializerMethodField()
    # review = ReviewSerializer()
    #
    # def get_article_review(self, obj):
    #     review_rate_data = []
    #     review_content_data = []
    #
    #     for reviews in obj.article.review_set.all():
    #         review_rate_data.append(reviews.review.rate)
    #         review_content_data.append(reviews.review.content)
    #
    #
    #     return {"rate" : review_rate_data, "content":review_content_data}

    class Meta:
        model = ArticleModel
        fields = '__all__'

    farm_name = serializers.CharField(required=True, min_length=2)
    title = serializers.CharField(required=True, min_length=4)
    display_article = serializers.BooleanField(default=True)

    def create(self, validated_data):
        print(validated_data)
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


class MyPageSerializer(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField(read_only=True)

    def get_userinfo(self,obj):
        return {
            "email": obj.user.email,
            "rank" :obj.user.userprofile.rank.rank_name,
            "birthday":obj.user.userprofile.birthday,
            "fullname": obj.user.userprofile.fullname,
            "location": obj.user.userprofile.location,
            "prefer": obj.user.userprofile.prefer,
            "gender": obj.user.userprofile.gender,
            "introduction": obj.user.userprofile.introduction,
            "phone_number": obj.user.userprofile.phone_number,
            "points":obj.user.userprofile.points,
            "profile_img": obj.user.userprofile.img.url,
        }
    class Meta:
        model = ArticleModel
        fields = [
            "id","user","article_category","farm_name","location","title","cost","requirement","period","img1","img2","img3",
            "desc","display_article","exposure_end_date","created_at","updated_at","userinfo"
        ]


class ArticleApplySerializer(serializers.ModelSerializer):


    def get_userinfo(self, obj):
        return {
            "email": obj.user.email,
            "rank" :obj.user.userprofile.rank.rank_name,
            "birthday":obj.user.userprofile.birthday,
            "fullname": obj.user.userprofile.fullname,
            "location": obj.user.userprofile.location,
            "prefer": obj.user.userprofile.prefer,
            "gender": obj.user.userprofile.gender,
            "introduction": obj.user.userprofile.introduction,
            "phone_number": obj.user.userprofile.phone_number,
            "points":obj.user.userprofile.points,
            # "profile_img": obj.user.userprofile.img
        }

    class Meta:
        model = ApplyModel
        fields = ["user", "article", "accept"]

    def create(self, validated_data):
        print(validated_data)
        apply = ApplyModel.objects.create(
            user=validated_data['user'],
            article = validated_data['article']

        )
        return apply


class UserApplySerializer(serializers.ModelSerializer):
    articleinfo = serializers.SerializerMethodField(read_only=True)
    userinfo = serializers.SerializerMethodField(read_only=True)

    def get_userinfo(self, obj):
        return {
            "email": obj.user.email,
            "fullname": obj.user.userprofile.fullname,
            "location": obj.user.userprofile.location,
            "prefer": obj.user.userprofile.prefer,
            "gender": obj.user.userprofile.gender,
            "rank": obj.user.userprofile.rank.rank_name,
            "age": obj.user.userprofile.age,
            "phone_number": obj.user.userprofile.phone_number,
            "img": obj.user.userprofile.img.url,
        }
    def get_articleinfo(self, obj):
        return {
            "article_id":obj.article.id,
            "farm_name":obj.article.farm_name,
            "location": obj.article.location ,
            "title": obj.article.title,
            "period": obj.article.period,
            "cost": obj.article.cost,
            "desc": obj.article.desc,
        }

    class Meta:
        model = ApplyModel

        fields = ["user","article","accept","articleinfo","userinfo"]



# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    articleinfo = serializers.SerializerMethodField(read_only=True)
    def get_articleinfo(self, obj):
        return {
            "title":obj.article.title,
            "period": obj.article.period,
        }
    class Meta:
        model = ReviewModel
        fields = ["id","user","article","rate","img1","img2","img3","content","created_at","updated_at","articleinfo"]
