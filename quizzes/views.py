from django.contrib.auth import get_user_model
from rest_framework import generics
from .models import Quiz, Question
from .serializers import QuizSerializer
from .youtube import download_audio
from .whisper_service import transcribe_audio
from .gemini_service import generate_quiz_from_transcript

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

        # MYA: Geändert - erst Transcript kurz speichern
        quiz.description = transcript[:500]
        quiz.save()

        print("STEP 4: Transcript im Quiz gespeichert")

        # MYA: Neu - Gemini erzeugt jetzt Quiz JSON
        print("STEP 5: Gemini startet jetzt")
        quiz_data = generate_quiz_from_transcript(transcript)

        print("STEP 6: Gemini fertig")
        print("Quiz Titel:", quiz_data["title"])

        # MYA: Neu - Quiz-Daten aus Gemini speichern
        quiz.title = quiz_data["title"]
        quiz.description = quiz_data["description"]
        quiz.save()

        # MYA: Neu - Fragen automatisch anlegen
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

        print("STEP 7: Fragen gespeichert")
        
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer