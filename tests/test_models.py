from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.models import Newspaper, Redactor, Commentary, Topic


class ModelTests(TestCase):
    def test_newspaper_str(self):
        publisher = Redactor.objects.create(
            username="test_username", password="test_password"
        )
        Topic.objects.create(name="Test")
        newspaper = Newspaper.objects.create(
            title="Test_newspaper",
            content="Test_content",
            publish_date="Test_date",
            topic_id=1,
        )
        newspaper.publishers.set([publisher])
        self.assertEquals(str(newspaper), f"{newspaper.title}")

    def test_redactor_str(self):
        redactor = Redactor.objects.create(
            username="test_username",
            password="test_password",
            first_name="first_test",
            last_name="last_test",
        )
        self.assertEquals(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})",
        )

