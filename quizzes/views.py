from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .gemini_service import (
    GeminiQuizGenerationError,
    generate_quiz_from_transcript,
)
from .models import Quiz, Question
from .serializers import QuizSerializer
from .whisper_service import transcribe_audio
from .youtube import download_audio


class QuizListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating quizzes for the authenticated user.
    """

    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all quizzes of the authenticated user ordered by creation date.
        """
        return Quiz.objects.filter(user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        Creates a new quiz from a YouTube URL.

        Validates the input, processes the video, generates quiz data,
        and returns the saved quiz. If Gemini fails, a 503 response is returned.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except GeminiQuizGenerationError as error:
            return Response(
            {"detail": str(error)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
        except Exception as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        """
        Saves the quiz, downloads the audio, transcribes it,
        generates quiz data, and stores the related questions.

        If any step fails, the created quiz is deleted again
        to avoid incomplete database entries.
        """
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
    """
    Handles retrieving, updating, and deleting a single quiz.
    Only the owner of the quiz is allowed to access it.
    """

    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the requested quiz if it belongs to the authenticated user.
        Raises 403 if the quiz belongs to another user.
        """
        quiz = get_object_or_404(Quiz, pk=self.kwargs["pk"])

        if quiz.user != self.request.user:
            raise PermissionDenied("Quiz gehört nicht dem Benutzer.")

        return quiz
    
class LatestQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quiz = Quiz.objects.filter(user=request.user).order_by("-created_at").first()

        if not quiz:
            return Response({"detail": "No quiz found"}, status=404)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data)