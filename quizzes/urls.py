from django.urls import path
from .views import QuizDetailView, QuizListCreateView, LatestQuizView


urlpatterns = [
    path("quizzes/", QuizListCreateView.as_view(), name="quiz-list-create"),
    path("quizzes/null/", LatestQuizView.as_view(), name="quiz-latest"),
    path("quizzes/<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
]