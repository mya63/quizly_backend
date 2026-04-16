from rest_framework import serializers
from .models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "question_options",
            "answer",
        ]

    def get_question_options(self, obj):
        return [
            obj.option_a,
            obj.option_b,
            obj.option_c,
            obj.option_d,
        ]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    # 👉 INPUT Feld
    youtube_url = serializers.URLField(write_only=True)

    # 👉 OUTPUT Feld (Doku-konform)
    video_url = serializers.CharField(source="youtube_url", read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "youtube_url",   # 👈 wichtig für POST
            "video_url",     # 👈 für Response
            "questions",
        ]

        read_only_fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]