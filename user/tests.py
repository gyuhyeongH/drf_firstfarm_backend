import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse('user_view')
        user_data = {
            "username": "test",
            "password": "password",
            "email": "test@testuser.com",
            "user_category": 2,
            "userprofile": [{
                "fullname": "testuser",
                "gender": "M",
                "birthday": "1995-01-01",
                "age": 28,
                "phone_number": "010-9900-0000",
                "location": "경기도",
                "introduction": "testuser",
                "prefer": "사과",
            }],
            "img": ["undefined"]
        }
        # response = self.client.post(url, json.dumps(user_data), content_type="application/json")
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 200)










# # Create your tests here.
# class TestView(TestCase):
#     def test_two_is_three(self):
#         self.assertEqual(2,3)
    
#     def test_two_is_two(self):
#         self.assertEqual(2,2)