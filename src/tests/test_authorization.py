from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestAuthUser(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="user@example.com", email="user@example.com", password="a-secure-password"
        )

        self.manager = User.objects.create_user(
            username="admin@example.com", email="admin@example.com", password="another-secure-password", is_staff=True
        )

    def test_user_login_successful(self):
        logged_in = self.client.login(username="user@example.com", password="a-secure-password")
        self.assertTrue(logged_in)

    def test_user_login_wrong_username(self):
        logged_in = self.client.login(username="wrong_user@example.com", password="a-secure-password")
        self.assertFalse(logged_in)

    def test_user_login_wrong_password(self):
        logged_in = self.client.login(username="user@example.com", password="wrong-password")
        self.assertFalse(logged_in)

    def test_user_access_admin_panel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_manager_access_admin_panel(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_access_index_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("translator:translate"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
