from django.conf import settings
from django.db import models


class Quiz(models.Model):
    """
    Stores a generated quiz for a specific user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transcript = models.TextField(blank=True)

    def __str__(self):
        """
        Returns the quiz title for admin and shell display.
        """
        return self.title


class Question(models.Model):
    """
    Stores a single question belonging to a quiz.
    """

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
        """
        Returns the question title for admin and shell display.
        """
        return self.question_title