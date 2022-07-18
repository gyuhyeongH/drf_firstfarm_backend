from django.shortcuts import render
import copy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article as ArticleModel
from .models import Apply as ApplyModel
from .models import Review as ReviewModel
from article.serializers import ArticleSerializer
from article.serializers import ArticleApplySerializer
from article.serializers import ReviewSerializer

class ArticleView(APIView):
    def get(self, request):
        locations = ['서울','인천']
        request_front = request.data.get('choice')
        articles = ArticleModel.objects.all()

        if request_front == '추천':
            recommend_articles = recommends(articles, request.user.userprofile.prefer)  # 추천 시스템 함수
            Response(recommend_articles, status=status.HTTP_200_OK)
        elif request_front in locations:
            location_articles = location_article(articles, request_front)  # 지역 별 함수
            return Response(location_articles, status=status.HTTP_200_OK)

        return Response(articles, status=status.HTTP_200_OK)


def recommends(articles, user_prefer):
    recommend_articles =[]
    article_info=[]
    for article in articles:
        article_info.append(article.desc)
    # 코랩에서 user_prefer,articles_info 이용한 코드 작성 밑 테스트 이후 배포할때 추가.
    return recommend_articles


def location_article(articles, request_front):
    location_articles=[]
    for article in articles:
        if request_front in article.location:
            location_articles.append(article)
    return location_articles


class ArticleDetailView(APIView):

    def get(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
    # authentication_classes = [JWTAuthentication]

        serializer = ArticleSerializer(article, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글이 작성되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, article_id):
        user = request.user
        article = ArticleModel.objects.get(id=article_id)
        serializer = ArticleSerializer(article, data=request.data, partial=True)

        # if user.is_anonymous:
        #     return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, article_id):
    #     user = request.user
    #     article = ArticleModel.objects.get(id=article_id)
    #     if user == article.user_id:
    #         return Response({"message": "게시글 마감 성공."}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"message": "게시글 마감 실패."}, status=status.HTTP_400_BAD_REQUEST)



class ArticleApplyView(APIView):

    def post(self, request, article_id):
        # user = request.user
        # article = ArticleModel.objects.get(id=article_id)
        serializer = ArticleApplySerializer(data=request.data)

        # if user.is_anonymous:
        #     return Response({"error": "로그인 후 이용해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "신청이 완료되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


#farm_mypage ~ 자신이 올린 공고 조회
class FarmMyPageView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        # user = request.user.id # 로그인 한 유저
        user = 2
        articles = ArticleModel.objects.filter(user=user) # 로그인 한 유저가 올린 공고들을 가져옴
        articles = ArticleSerializer(articles, many=True).data

        return Response(articles, status=status.HTTP_200_OK) # 로그인 한 유저가 올린 공고들의 serializer 를 넘겨줌

    # 삭제 부분은 디테일 페이지에서 구현 되어있어서 우선 지워둠.
    # def delete(self, request, article_id):
    #     user = request.user.id # 로그인 한 유저
    #     article = ArticleModel.objects.filter(id=article_id) # 삭제하려는 article을 가져옴
    #     if user == article.user_id: #로그인 한 유저가 해당 article의 작성자가 맞다면
    #         article.delete() # 삭제
    #         return Response({"message": "공고가 삭제되었습니다."}, status=status.HTTP_200_OK)
    #
    #     else:
    #         return Response({"message": "공고 삭제를 실패했습니다."},status=status.HTTP_400_BAD_REQUEST)

# farm_mypage ~ 자신이 올린 공고중 특정 공고에 지원한 신청자 조회
class FarmApplyView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request,article_id):
        applicants = ApplyModel.objects.filter(article=article_id) # 해당 공고에 지원한 지원정보들을 가져옴
        applicants = ArticleApplySerializer(applicants, many=True).data

        # applicants = applicants.get(user_id = request.user_id)
        # for i=0; i<user.length ; i++ :
        #     users += applicants[i].article # obj
        print(applicants)

        return Response(applicants, status=status.HTTP_200_OK) # 해당 공고에 지원한 Applyserializer 정보를 넘겨줌


#farmer_mypage ~ 신청자가 다녀온 공고 조회, 다녀온 공고의 리뷰 작성, 수정, 삭제
class FarmerMyPageView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        # user = request.user.id # 로그인 한 유저
        user = 1
        apllies = ApplyModel.objects.filter(user=user,accept=True) # 로그인 한 유저가 다녀온 공고들을 가져옴 , queryset
        # for i=0; i<articles.length ; i++ :
        #     articles += applies[i].article # obj
        apllies = ArticleApplySerializer(apllies, many=True).data
        print(apllies)

        return Response(apllies, status=status.HTTP_200_OK) # 로그인 한 유저가 다녀온 공고들의 serializer 를 넘겨줌

    def post(self, request, article_id):
        data = copy.deepcopy(request.data)
        # data["user"] = request.user.id
        data["user"] = 1
        data["article"] = article_id
        data["content"] = request.data.get("content", "") #review 내용
        data["rate"] = request.data.get("rate","") # 평점
        data["img1"] = request.data.get("img1","") # 이 부분 테스트 해보고 2,3 까지 작성
        data["img2"] = request.data.get("img2", "")  # 이 부분 테스트 해보고 2,3 까지 작성
        data["img3"] = request.data.get("img3", "")  # 이 부분 테스트 해보고 2,3 까지 작성
        review_serializer = ReviewSerializer(data=data)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response({"result": "리뷰 작성 완료!"}, status=status.HTTP_200_OK)
        else:
            return Response({"result": "리뷰 작성 실패!"}, status=status.HTTP_400_BAD_REQUEST)

        # serializer = ReviewSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"message": "리뷰가 작성되었습니다."}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


    # 업데이트
    def put(self, request, review_id):
        review = ReviewModel.objects.get(id=review_id)
        review_serializer = ReviewSerializer(review, data=request.data, partial=True)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(review_serializer.data, status=status.HTTP_200_OK)
        return Response({"result": "리뷰 수정 실패!"}, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, review_id):
        # user = request.user.id
        user = 1
        review = ReviewModel.objects.get(id=review_id)
        if user == review.user_id:
            review.delete()
            return Response({"message": "리뷰 삭제 완료."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "리뷰 삭제 실패."}, status=status.HTTP_400_BAD_REQUEST)

#farmer_mypage ~ 신청자가 작성한 리뷰 조회
class FarmerReviewView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        # user = request.user.id # 로그인 한 유저
        user = 1
        reviews = ReviewModel.objects.filter(user=user) # 로그인 한 유저가 작성한 리뷰들을 가져옴
        serialized_data = ReviewSerializer(reviews, many=True).data  # queryset
        return Response(serialized_data, status=status.HTTP_200_OK)


