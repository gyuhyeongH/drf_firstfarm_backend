from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Apply as ApplyModel
from article.models import Review as ReviewModel


class ArticleGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    article_review = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    def get_rank(self, obj):
        rank_data = []
        rank = obj.user.userprofile.rank.rank_name
        rank_data.append(rank)
        return {"rank": rank_data}

    def get_phone_number(self, obj):
        phone_number_data = []
        phone_number = obj.user.userprofile.phone_number
        phone_number_data.append(phone_number)
        return {"phone_number": phone_number_data}

    def get_article_review(self, obj):
        review_rate_data = []
        review_content_data = []
        review_user_data = []
        review_img_data = []
        for reviews in obj.review_set.all():
            review_rate_data.append(reviews.rate)
            review_content_data.append(reviews.content)
            review_user_data.append(reviews.user.username)
            review_img_data.append(reviews.img1.url)
            review_img_data.append(reviews.img2.url)
            review_img_data.append(reviews.img3.url)
        return {"rate" : review_rate_data, "content":review_content_data, "review_user":review_user_data, "review_img":review_img_data}



    class Meta:
        model = ArticleModel
        fields = [
            "id", "user", "article_category", "farm_name", "location", "title", "cost", "requirement", "period", "img1",
            "img2", "img3",
            "desc", "display_article", "exposure_end_date", "created_at", "updated_at", "article_review", "phone_number", "rank",
        ]

    farm_name = serializers.CharField(required=True, min_length=2)
    title = serializers.CharField(required=True, min_length=4)
    display_article = serializers.BooleanField(default=True)

    def create(self, validated_data):
        article = ArticleModel(**validated_data)
        article.save()
        return article
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
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
            "desc","exposure_end_date","created_at","updated_at","userinfo"
        ]


class ArticleApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplyModel
        fields = ["user", "article", "accept"]

    def create(self, validated_data):
        apply = ApplyModel.objects.create(
            user=validated_data['user'],
            article = validated_data['article']
        )
        return apply


class UserApplySerializer(serializers.ModelSerializer):
    articleinfo = serializers.SerializerMethodField(read_only=True)
    userinfo = serializers.SerializerMethodField(read_only=True)
    reviewinfo = serializers.SerializerMethodField(read_only=True)

    def get_userinfo(self, obj):
        return {
            "email": obj.user.email,
            "fullname": obj.user.userprofile.fullname,
            "location": obj.user.userprofile.location,
            "prefer": obj.user.userprofile.prefer,
            "gender": obj.user.userprofile.gender,
            "rank": obj.user.userprofile.rank.rank_name,
            "birthday": obj.user.userprofile.birthday,
            "phone_number": obj.user.userprofile.phone_number,
            "profile_img": obj.user.userprofile.img.url,
            "points": obj.user.userprofile.points,
            "introduction": obj.user.userprofile.introduction,
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
            "img1":obj.article.img1.url,
        }
    def get_reviewinfo(self,obj):
        temp = obj.user.review_set.all() #내가 쓴 리뷰
        temp_array = [] # 내가 쓴 리뷰의 article

        for i in range(0, len(temp)):
            temp_array.append(temp[i].article)

        if(temp_array.count(obj.article) > 0 ):
            return False
        else:
            return True

    class Meta:
        model = ApplyModel
        fields = ["id","user","article","accept","articleinfo","userinfo","reviewinfo"]


# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    articleinfo = serializers.SerializerMethodField(read_only=True)
    def get_articleinfo(self, obj):
        return {
            "title":obj.article.title,
            "period": obj.article.period,
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = ReviewModel
        fields = ["id","user","article","rate","img1","img2","img3","content","created_at","updated_at","articleinfo"]

class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyModel
        fields = "__all__"