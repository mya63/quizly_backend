from django.conf import settings
from django.db import models



class Quiz(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    youtube_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    transcript = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_title = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_title