from django.contrib.auth import get_user_model
from rest_framework import generics
from .models import Quiz, Question
from .serializers import QuizSerializer
from .youtube import download_audio
from .whisper_service import transcribe_audio


class QuizListCreateView(generics.ListCreateAPIView):
        queryset = Quiz.objects.all().order_by("-created_at")
        serializer_class = QuizSerializer

        def perform_create(self, serializer):
            user = get_user_model().objects.first()
            quiz = serializer.save(user=user)

            audio_path = download_audio(quiz.youtube_url)
            print("STEP 1: Audio gespeichert:", audio_path)

            print("STEP 2: Whisper startet jetzt")
            transcript = transcribe_audio(audio_path)

            print("STEP 3: Whisper fertig")
            print("Transcript:", transcript[:500])

            quiz.description = transcript[:500]
            quiz.save()

            print("STEP 4: Transcript im Quiz gespeichert")

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer