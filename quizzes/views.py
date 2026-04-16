from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .gemini_service import (
    GeminiQuizGenerationError,
    generate_quiz_from_transcript,
)
from .models import Quiz, Question
from .serializers import QuizSerializer
from .whisper_service import transcribe_audio
from .youtube import download_audio


class QuizListCreateView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except GeminiQuizGenerationError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception:
            return Response(
                {"detail": "Quiz konnte nicht erstellt werden."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        quiz = serializer.save(user=self.request.user)

        try:
            audio_path = download_audio(quiz.youtube_url)
            transcript = transcribe_audio(audio_path)

            quiz.transcript = transcript
            quiz.save()

            quiz_data = generate_quiz_from_transcript(transcript)

            quiz.title = quiz_data["title"]
            quiz.description = quiz_data["description"]
            quiz.save()

            for item in quiz_data["questions"]:
                Question.objects.create(
                    quiz=quiz,
                    question_title=item["question_title"],
                    option_a=item["question_options"][0],
                    option_b=item["question_options"][1],
                    option_c=item["question_options"][2],
                    option_d=item["question_options"][3],
                    answer=item["answer"],
                )
        except Exception:
            quiz.delete()
            raise


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        quiz = get_object_or_404(Quiz, pk=self.kwargs["pk"])

        if quiz.user != self.request.user:
            raise PermissionDenied("Quiz gehört nicht dem Benutzer.")

        return quiz