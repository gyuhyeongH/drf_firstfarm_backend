import tempfile

from faker import Faker
from PIL import Image
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework.test import APITestCase

from user.models import User, UserProfile, Rank, UserCategory
from article.models import ArticleCategory, Article
from article.serializers import ArticleSerializer


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file


class ArticleTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username': 'testusername', 'password': 'testpassword'}
        cls.article_data = {
            "article_category": 1,
            "farm_name": "test",
            "location": "test",
            "title": "test",
            "cost": "test",
            "requirement": "test",
            "period": "test",
            "desc": "test",
            "img1": None,
            "img2": None,
            "img3": None,
        }
        cls.article_update_data = {
            "farm_name": "test2",
            "location": "test2",
            "title": "test2",
        }
        cls.user = User.objects.create_user('testusername', 'testpassword')
        cls.usercategory = UserCategory.objects.create(name="test")
        cls.user.user_category = cls.usercategory
        cls.user.save()
        cls.category = ArticleCategory.objects.create(name="test")
        cls.rank = Rank.objects.create(rank_name='test1')
        cls.userprofile = UserProfile.objects.create(user_id=1, prefer="test", rank_id=1, fullname="test",
                                                     location="서울", gender="M",
                                                     age=11, birthday="1995-01-25", img="", phone_number="11", points=0)
        cls.article = Article.objects.create(article_category_id=1, farm_name="aaaa", location='aaaaa', title='aaaaa',
                                             cost='aaaaaa',
                                             user_id=1, requirement='aaaaa', period='aaaaa', desc='aaaaa', img1=None,
                                             img2=None, img3=None)

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    def test_create_article(self):
        response = self.client.post(
            path=reverse('article_create_view'),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_article(self):
        response = self.client.put(
            path=reverse('article_detail_view', args=[1]),
            data=self.article_update_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_article_apply(self):
        response = self.client.post(
            path=reverse('article_apply_view', args=[1]),
            data={},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)


class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles = []
        cls.category = ArticleCategory.objects.create(name="test")
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            cls.rank = Rank.objects.create(rank_name='test1')
            cls.userprofile = UserProfile.objects.create(user_id=i+1, prefer="test", rank_id=1, fullname="test",
                                                     location="서울", gender="M",
                                                     age=11, birthday="1995-01-25", img="", phone_number=i, points=0)
            cls.articles.append(Article.objects.create(article_category_id=1, farm_name="aaaa", location='aaaaa',
                                                       title=cls.faker.sentence()[:30], cost='aaaaaa',
                                                       user=cls.user, requirement='aaaaa', period='aaaaa',
                                                       desc=cls.faker.text(), img1=None, img2=None, img3=None, display_article=True))

    def test_get_article(self):
        url = reverse('article_view')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 10)

    def test_get_article_detail(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer = ArticleSerializer(article).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)



