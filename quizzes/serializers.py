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

    Accepts both youtube_url and fake_video_url as input.
    Returns video_url in the documented response format.
    """

    questions = QuestionSerializer(many=True, read_only=True)
    youtube_url = serializers.URLField(required=False)
    fake_video_url = serializers.URLField(write_only=True, required=False)
    video_url = serializers.CharField(source="youtube_url", read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "youtube_url",
            "fake_video_url",
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

    def validate(self, attrs):
        fake_video_url = attrs.pop("fake_video_url", None)
        youtube_url = attrs.get("youtube_url")

        if not youtube_url and fake_video_url:
            attrs["youtube_url"] = fake_video_url

        if not attrs.get("youtube_url"):
            raise serializers.ValidationError({
                "fake_video_url": "This field is required."
            })

        return attrs