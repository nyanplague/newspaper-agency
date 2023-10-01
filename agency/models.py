from django.contrib.auth.models import AbstractUser
from django.db import models

from newspaper_agency import settings


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Topic(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=64, unique=True)
    content = models.TextField()
    publish_date = models.DateTimeField()
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="newspapers"
    )
    publishers = models.ManyToManyField(Redactor, related_name="newspapers")

    def __str__(self):
        return self.title


class Commentary(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        verbose_name_plural = "comments"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    newspaper = models.ForeignKey(
        Newspaper, on_delete=models.CASCADE, related_name="comments"
    )
