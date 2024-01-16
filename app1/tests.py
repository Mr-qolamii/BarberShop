from django.test import TestCase, Client

from app1.models import *


class App1TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tset', tell='+989904761632', password='test@1234')

    def test_register_response(self):
        response = self.client.login(username='tset', password='test@1234')
        self.assertTrue(response)

    def test_logout_response(self):
        response = self.client.login(username='tset', password='test@1234')
        response = self.client.get('http://127.0.0.1:8000/logout/', ).status_code
        self.assertIs(response, 200)

    def test_signup_response(self):
        response = self.client.post('http://127.0.0.1:8000/',
                                    data={'username': 'tset2',
                                          'tell': '+989904761638',
                                          'password': 'test2@1234',
                                          'password_2': 'test2@1234'
                                          }
                                    ).status_code
        self.assertIs(response, 201)
