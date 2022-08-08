from django.db.models import Q
import copy
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user.models import UserProfile as UserProfileModel
from .models import Article as ArticleModel
from .models import Apply as ApplyModel
from .models import Review as ReviewModel
from article.serializers import ArticleSerializer

from article.serializers import ArticleApplySerializer, UserApplySerializer, MyPageSerializer
from article.serializers import ReviewSerializer

try:
    from konlpy.tag import Mecab
    from gensim.test.utils import common_texts
    from gensim.models.doc2vec import Doc2Vec, TaggedDocument
except:
    pass


# 평가점수를 point에 더하고 랭크를 변경하는 함수
def get_rate_rank_point(user, rate):
    current_points = user.userprofile.points + rate
    UserProfileModel.objects.filter(user=user).update(points=current_points)

    if 5 <= current_points < 10:
        UserProfileModel.objects.filter(user_id=user).update(rank_id=1)

    elif 10 <= current_points < 15:
        UserProfileModel.objects.filter(user_id=user).update(rank_id=2)

    elif 15 <= current_points < 20:
        UserProfileModel.objects.filter(user_id=user).update(rank_id=3)

    elif current_points >= 20:
        UserProfileModel.objects.filter(user_id=user).update(rank_id=4)


class ArticleView(APIView):

    def get(self, request):
        request_location_choice = request.headers.get('choice') if request.headers.get('choice') is not None else ""
        request_article_category = request.headers.get('category') if request.headers.get('category') is not None else ""

        location_list = ['서울', '경기', '인천', '강원', '대전', '세종', '충청남도', '충청북도', '부산', '울산', '경상남도', '경상북도', '대구', '광주',
                         '전라남도', '전라북도', '제주도']

        if request_location_choice != "":
            request_location_choice = location_list[int(request_location_choice)]

        if request_article_category == '':
            articles = ArticleModel.objects.filter(Q(location__contains=request_location_choice) & Q(display_article=True))
            articles_serializer = ArticleSerializer(articles, many=True).data

            return Response(articles_serializer, status=status.HTTP_200_OK)

        elif request_article_category == '3':
            if request.user:
                articles = ArticleModel.objects.filter(display_article=True)
                recommend_articles = recommends(articles, request.user.userprofile.prefer)  # 추천 시스템 함수
                recommend_articles_serializer = ArticleSerializer(recommend_articles, many=True).data

                return Response(recommend_articles_serializer, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


        else:
            articles = ArticleModel.objects.filter(
                Q(article_category=request_article_category) & Q(location__contains=request_location_choice) & Q(
                    display_article=True))
            articles_serializer = ArticleSerializer(articles, many=True).data

            return Response(articles_serializer, status=status.HTTP_200_OK)


def recommends(articles, user_prefer):
    recommend_articles = []

    article_info = [article.desc for article in articles]
    try:
        mecab = Mecab()
        tmp_list = [[] for _ in range(len(article_info))]
        stopwords = []

        for i in range(0, len(article_info)):
            tmp = mecab.nouns(article_info[i])
            tokens = []
            for token in tmp:
                if not token in stopwords:
                    tokens.append(token)
            tmp_list[i] = tokens
            # article 형태소 분석 완료.

        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(tmp_list)]

        model = Doc2Vec(documents, vector_size=10, window=1, epochs=10, min_count=0, workers=4)

        prefer = mecab.nouns(user_prefer)

        inferred_doc_vec = model.infer_vector(prefer)
        most_similar_docs = model.docvecs.most_similar([inferred_doc_vec], topn=10)

        for index, similarity in most_similar_docs:
            recommend_articles.append(articles[index])
    except:
        pass
    return recommend_articles


class ArticleSearchView(APIView):
    def get(self, request):
        search_text = request.GET.get('search_text', '')
        articles = ArticleModel.objects.filter(Q(title__icontains=search_text) | Q(desc__icontains=search_text) | Q(display_article=True))
        articles_serializer = ArticleSerializer(articles, many=True).data

        return Response(articles_serializer, status=status.HTTP_200_OK)


# Create your views here.
class ArticleDetailView(APIView):

    def get(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)

        serializer = ArticleSerializer(article).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # 게시글 작성 시 마다 3점 추가

            get_rate_rank_point(request.user, 3)  # 임의 user1로 테스트
            return Response({"message": "게시글이 작성되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)

        if article.user.id == request.user.id:
            article_serializer = ArticleSerializer(article, data=request.data, partial=True)
   
            if article_serializer.is_valid():
                article_serializer.save()

                return Response({"message": "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)

            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        user = request.user.id
        article = ArticleModel.objects.get(id=article_id)
        if user == article.user.id:
            article.display_article = False
            article.save()
            # print(article.display_article)
            return Response({"message": "게시글 마감 성공."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "게시글 마감 실패."}, status=status.HTTP_400_BAD_REQUEST)




class ArticleApplyView(APIView):

    def post(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        data = {"article": article.id, "user": request.user.id}
        serializer = ArticleApplySerializer(data=data, partial=True)


        if serializer.is_valid():
            get_rate_rank_point(request.user, 3)  # 테스트 용 user_id 1 임의로 전달
            serializer.save()

            return Response({"message": "신청이 완료되었습니다."}, status=status.HTTP_200_OK)
        else:

            return Response({"message": f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


# farm_mypage ~ 자신이 올린 공고 조회
class FarmMyPageView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user.id # 로그인 한 유저
        # user = 2
        articles = ArticleModel.objects.filter(user=user)  # 로그인 한 유저가 올린 공고들을 가져옴
        articles = MyPageSerializer(articles, many=True).data
        return Response(articles, status=status.HTTP_200_OK)  # 로그인 한 유저가 올린 공고들의 serializer 를 넘겨줌

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

    def get(self, request, article_id):
        applicants = ApplyModel.objects.filter(article=article_id)  # 해당 공고에 지원한 지원정보들을 가져옴
        applicants = ArticleApplySerializer(applicants, many=True).data
        return Response(applicants, status=status.HTTP_200_OK)  # 해당 공고에 지원한 ArticleApplyserializer 정보를 넘겨줌


# farmer_mypage ~ 신청자가 다녀온 공고 조회, 다녀온 공고의 리뷰 작성, 수정, 삭제
class FarmerMyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id # 로그인 한 유저
        apllies = ApplyModel.objects.filter(user=user, accept=True)  # 로그인 한 유저가 다녀온 공고들을 가져옴 , queryset
        apllies = UserApplySerializer(apllies, many=True).data
        print(apllies)

        return Response(apllies, status=status.HTTP_200_OK)  # 로그인 한 유저가 다녀온 공고들의 UserApplyserializer 정보를 넘겨줌

    def post(self, request, article_id):
        data = copy.deepcopy(request.data)
        data["user"] = request.user
        data["article"] = article_id
        data["content"] = request.data.get("content", "")  # review 내용
        data["rate"] = request.data.get("rate", "")  # 평점
        data["img1"] = request.data.get("img1", "")
        data["img2"] = request.data.get("img2", "")
        data["img3"] = request.data.get("img3", "")
        review_serializer = ReviewSerializer(data=data)
        rate = int(data["rate"]) - 3
        if review_serializer.is_valid():
            review_serializer.save()
            # 리뷰 작성자 에게는 포인트 3점 추가
            farmer = request.user.id
            get_rate_rank_point(farmer,3)
            # # 리뷰의 평가점수를 농장주에게 추가
            farm = ArticleModel.objects.filter(id=article_id).values("user_id")[0].get("user_id")
            get_rate_rank_point(farm, rate)
            return Response({"result": "리뷰 작성 완료!"}, status=status.HTTP_200_OK)
        else:
            return Response({"result": "리뷰 작성 실패!"}, status=status.HTTP_400_BAD_REQUEST)

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
        user = request.user.id
        review = ReviewModel.objects.get(id=review_id)
        if user == review.user_id:
            review.delete()
            return Response({"message": "리뷰 삭제 완료."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "리뷰 삭제 실패."}, status=status.HTTP_400_BAD_REQUEST)


# farmer_mypage ~ 신청자가 작성한 리뷰 조회
class FarmerReviewView(APIView):
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user.id # 로그인 한 유저
        reviews = ReviewModel.objects.filter(user=user)  # 로그인 한 유저가 작성한 리뷰들을 가져옴
        serialized_data = ReviewSerializer(reviews, many=True).data  # queryset
        return Response(serialized_data, status=status.HTTP_200_OK)
