from rest_framework import serializers

from .models import Question, Quiz


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz questions.

    Combines the four stored answer options into one list
    for the API response format.
    """

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
        """
        Returns the four stored answer options as a list.

        Args:
            obj (Question): Question instance.

        Returns:
            list[str]: List of answer options.
        """
        return [
            obj.option_a,
            obj.option_b,
            obj.option_c,
            obj.option_d,
        ]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for quizzes.

    Accepts url from the frontend request.
    Returns video_url in the API response.
    """

    questions = QuestionSerializer(many=True, read_only=True)
    video_url = serializers.URLField(source="url", read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "url",
            "video_url",
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