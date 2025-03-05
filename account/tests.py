from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestLogin(TestCase):
    """Tests for the login view."""

    def test_login_failed(self):
        """Posting login with the wrong password fails."""
        User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_successful(self):
        """Users can authenticate successfully on /login page."""
        User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class TestDashboard(TestCase):
    """Tests for the dashboard view."""

    def test_dashboard_requires_login(self):
        """The dashboard page requires login."""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/account/")

    def test_dashboard_accessible(self):
        """The dashboard page is accessible after login."""
        user = User.objects.create_user(username="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard.html")
