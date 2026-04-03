from django.contrib.auth import get_user_model
from rest_framework import generics
from .models import Quiz, Question
from .serializers import QuizSerializer
from .youtube import download_audio


class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all().order_by("-created_at")
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        user = get_user_model().objects.first()
        quiz = serializer.save(user=user)

        audio_path = download_audio(quiz.youtube_url)
        
        print("Audio gespeichert:", audio_path)



        # 🔥 TEST: Eine Dummy-Frage erstellen
        Question.objects.create(
            quiz=quiz,
            question_title="Test Frage",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            answer="A",
        )

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer