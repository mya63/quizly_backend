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

    Accepts video_url (API docs),
    fake_video_url (academy frontend),
    and youtube_url (legacy frontend).

    Returns video_url in the documented response format.
    """

    questions = QuestionSerializer(many=True, read_only=True)

    youtube_url = serializers.URLField(required=False, write_only=True)
    fake_video_url = serializers.URLField(required=False, write_only=True)
    video_url = serializers.URLField(required=False)

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
            "questions",
        ]

    def validate(self, attrs):
        youtube_url = attrs.pop("youtube_url", None)
        fake_video_url = attrs.pop("fake_video_url", None)
        video_url = attrs.get("video_url")

        final_url = (
            video_url
            or fake_video_url
            or youtube_url
        )

        if not final_url:
            raise serializers.ValidationError({
                "video_url": "This field is required."
            })

        attrs["youtube_url"] = final_url
        attrs["video_url"] = final_url

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["video_url"] = instance.youtube_url
        return data