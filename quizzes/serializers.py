from rest_framework import serializers
from .models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "answer",
        ]



class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "user",
            "title",
            "description",
            "transcript",
            "youtube_url",
            "created_at",
            "questions",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "questions",
            "title",
            "description",
            "transcript",
        ]