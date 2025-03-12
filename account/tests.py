from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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


class TestLogout(TestCase):
    """Tests for the logout view."""

    def test_logout(self):
        """Users can log out successfully."""
        user = User.objects.create_user(username="testuser")
        self.client.force_login(user)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/logout_done")

    def test_logout_done_page(self):
        """The logout done page is accessible."""
        response = self.client.get(reverse("logout_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/logged_out.html")


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


class TestRegister(TestCase):
    """Tests for the register view."""

    def test_register_page(self):
        """The register page is accessible."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")

    def test_register_user(self):
        """Users can register successfully."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password": "testpassword",
                "password2": "testpassword",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/register_done/")
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_register_done_page(self):
        """The register done page is accessible."""
        response = self.client.get(reverse("register_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register_done.html")

    def test_register_password_mismatch(self):
        """On the register page, passwords must match."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password": "testpassword",
                "password2": "wrongpassword",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords don&#x27;t match.")
        self.assertEqual(User.objects.count(), 0)


class TestUserEdit(TestCase):
    """Tests for the edit view."""

    def test_edit_page(self):
        """The edit page is accessible."""
        user = User.objects.create_user(username="testuser")
        self.client.force_login(user)
        response = self.client.get(reverse("edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/edit.html")

    def test_edit_user(self):
        """Users can edit their profile."""
        user = User.objects.create_user(username="testuser")
        self.client.force_login(user)
        response = self.client.post(
            reverse("edit"),
            {
                "username": "newtestuser",
                "first_name": "New Test",
                "last_name": "New User",
                "email": "newtest@example.com"
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/")
        user.refresh_from_db()
        self.assertEqual(user.username, "newtestuser")
        self.assertEqual(user.first_name, "New Test")
        self.assertEqual(user.last_name, "New User")
        self.assertEqual(user.email, "newtest@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
