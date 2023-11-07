from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from agency.models import Newspaper, Redactor, Topic


class PrivateRedactorTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_create_redactor(self):
        form_data = {
            "username": "test_username",
            "years_of_experience": "8",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "password_test",
            "password2": "password_test",
        }

        self.client.post(reverse("agency:redactor-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(
            new_user.years_of_experience, int(form_data["years_of_experience"])
        )


class PrivateNewspaperCreateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password_test"
        )
        self.client.force_login(self.user)

    def test_create_newspaper(self):
        publisher = Redactor.objects.create(
            username="test_username", password="test_password"
        )
        topic = Topic.objects.create(name="Test")

        form_data = {
            "title": "test_title",
            "content": "test_content",
            "topic": topic.id,
            "publish_date": "2023-04-15 14:37:22",
            "publishers": [publisher.id],
        }

        self.client.post(reverse("agency:newspaper-create"), data=form_data)
        new_newspaper = Newspaper.objects.get(title=form_data["title"])

        self.assertEqual(new_newspaper.title, form_data["title"])
        self.assertEqual(new_newspaper.content, form_data["content"])
