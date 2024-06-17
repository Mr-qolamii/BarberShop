from django.test import TestCase, Client
import random

from app1.models import *


class App1TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tset', tell='+989904761632', password='test@1234')

    def test_register_response(self):
        response = self.client.post('http://127.0.0.1:8000/register/',
                                    data={"username": 'tset', "password": 'test@1234'},
                                    headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                             "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
        self.assertTrue(response)

    def test_logout_response(self):
        self.client.login(username='tset', password='test@1234')
        response = self.client.post('http://127.0.0.1:8000/register/',
                                    data={"username": 'tset', "password": 'test@1234'},
                                    headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                             "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})
        response = self.client.get('http://127.0.0.1:8000/logout/', ).status_code
        self.assertIs(response, 200)

