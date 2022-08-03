# from django.urls import reverse
# from rest_framework.test import APITestCase
#
# from user.models import User, UserCategory, Rank
#
#
# # 회원가입 테스트
# class UserRegistrationTest(APITestCase):
#     def setUp(self):
#         # 임시 모델 테이블 생성
#         UserCategory.objects.create(name="농장주")
#         UserCategory.objects.create(name="여름지기")
#
#         Rank.objects.create(rank_name="새싹")
#
#     def test_registration(self):
#         url = reverse('user_view')
#         # 데이터 설계
#         user_data = {
#             'username': 'test1234',
#             'password': 'password',
#             'email': 'test1234@testuser.com',
#             'user_category': 2,
#             'userprofile': {
#                 "fullname": "testuser",
#                 "gender": "M",
#                 "birthday": "1995-01-01",
#                 "age": 28,
#                 "phone_number": "010-9900-0000",
#                 "location": "경기도",
#                 "introduction": "testuser",
#                 "prefer": "사과"
#                 },
#             'img': "undefined"
#         }
#
#         response = self.client.post(url, user_data, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, 200)
#
#
# # 토큰 로그인 테스트
# class LoginUserTest(APITestCase):
#     def setUp(self):
#         self.data = {
#             'username': 'testuser',
#             'password': 'testpassword',
#             'email': 'test1234@testuser.com',
#             'user_category': 2,
#             'userprofile': {
#                 "fullname": "testuser",
#                 "gender": "M",
#                 "birthday": "1995-01-01",
#                 "age": 28,
#                 "phone_number": "010-9900-0000",
#                 "location": "경기도",
#                 "introduction": "testuser",
#                 "prefer": "사과",
#                 'img': "undefined"
#                 },
#         }
#         self.user = User.objects.create_user('testuser', 'testpassword')
#
#     def test_login(self):
#         response = self.client.post(reverse("token_obtain_pair"), self.data, format='json')
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_user_data(self):
#         access_token = self.client.post(reverse("token_obtain_pair"), self.data, format='json').data['access']
#         response = self.client.get(
#             path=reverse("user_view"),
#             HTTP_AUTHORIZATION=f"Bearer {access_token}"
#         )
#         # self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['username'], self.data['username'])
#
