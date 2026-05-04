import json
import time

from django.conf import settings
from google import genai
from pydantic import BaseModel, Field, ValidationError

class GeminiQuizGenerationError(Exception):
    """
    Raised when quiz generation with Gemini fails.
    """


class QuizQuestionSchema(BaseModel):
    """
    Validation schema for a single quiz question.
    """

    question_title: str = Field(min_length=5)
    question_options: list[str] = Field(min_length=4, max_length=4)
    answer: str = Field(min_length=1)


class QuizSchema(BaseModel):
    """
    Validation schema for a complete quiz.
    """

    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=150)
    questions: list[QuizQuestionSchema] = Field(min_length=10, max_length=10)


def build_quiz_prompt(transcript):
    """
    Builds the Gemini prompt from a transcript.

    Args:
        transcript (str): The transcribed audio text.

    Returns:
        str: Prompt text for Gemini.
    """
    return f"""
Generate a quiz from this transcript.

Return ONLY valid JSON.

Requirements:
- title: short and clear
- description: maximum 150 characters
- questions: exactly 10
- every question must contain:
  - question_title
  - question_options (exactly 4 strings)
  - answer
- answer must exactly match one of question_options
- no duplicate questions
- no markdown fences
- no explanations outside JSON
- use only information found in the transcript

Transcript:
{transcript}
""".strip()


def validate_quiz_logic(data):
    """
    Validates quiz logic after schema validation.

    Checks that each question has exactly four unique options
    and that the answer is included in the options.

    Args:
        data (dict): Generated quiz data.

    Returns:
        dict: Validated quiz data.

    Raises:
        GeminiQuizGenerationError: If logical validation fails.
    """
    for question in data["questions"]:
        options = question["question_options"]

        if len(options) != 4:
            raise GeminiQuizGenerationError("Eine Frage hat nicht genau 4 Optionen.")
        if len(set(options)) != 4:
            raise GeminiQuizGenerationError(
                "Eine Frage enthält doppelte Optionen."
            )
        if question["answer"] not in options:
            raise GeminiQuizGenerationError(
                "Antwort ist nicht in den Optionen enthalten."
            )

    return data


def get_retry_wait_time(attempt):
    """
    Returns the retry wait time for the current Gemini attempt.

    Args:
        attempt (int): Current retry attempt.

    Returns:
        int: Waiting time in seconds.
    """
    return 5 * (attempt + 1)


def build_dummy_quiz():
    """
    Returns a fallback quiz if Gemini is unavailable.

    Returns:
        dict: Static quiz data for frontend and backend testing.
    """
    return {
        "title": "Dummy Quiz",
        "description": "Dieses Quiz wurde als Fallback ohne Gemini erstellt.",
        "questions": [
            {
                "question_title": "What is 2 + 2?",
                "question_options": ["3", "4", "5", "6"],
                "answer": "4",
            },
            {
                "question_title": "What color is the sky on a clear day?",
                "question_options": ["Blue", "Green", "Red", "Yellow"],
                "answer": "Blue",
            },
            {
                "question_title": "Which animal barks?",
                "question_options": ["Cat", "Dog", "Fish", "Bird"],
                "answer": "Dog",
            },
            {
                "question_title": "Which season is usually the coldest?",
                "question_options": ["Summer", "Winter", "Spring", "Autumn"],
                "answer": "Winter",
            },
            {
                "question_title": "How many days are in a week?",
                "question_options": ["5", "6", "7", "8"],
                "answer": "7",
            },
            {
                "question_title": "Which one is a fruit?",
                "question_options": ["Carrot", "Potato", "Apple", "Onion"],
                "answer": "Apple",
            },
            {
                "question_title": "What do bees make?",
                "question_options": ["Milk", "Honey", "Bread", "Juice"],
                "answer": "Honey",
            },
            {
                "question_title": "Which planet do we live on?",
                "question_options": ["Mars", "Venus", "Earth", "Jupiter"],
                "answer": "Earth",
            },
            {
                "question_title": "How many months are in a year?",
                "question_options": ["10", "11", "12", "13"],
                "answer": "12",
            },
            {
                "question_title": "Which one can fly?",
                "question_options": ["Stone", "Chair", "Airplane", "Table"],
                "answer": "Airplane",
            },
        ],
    }


def generate_quiz_from_transcript(transcript):
    api_key = settings.GEMINI_API_KEY

    

    if not api_key:
        raise GeminiQuizGenerationError("GEMINI_API_KEY ist nicht gesetzt.")

    client = genai.Client(api_key=api_key)
    prompt = build_quiz_prompt(transcript)


    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": QuizSchema.model_json_schema(),
                },
            )

            try:
                quiz_data = QuizSchema.model_validate_json(response.text).model_dump()
                return validate_quiz_logic(quiz_data)

            except ValidationError:
                parsed_data = json.loads(response.text)

                if "description" in parsed_data:
                    parsed_data["description"] = parsed_data["description"][:150]

                quiz_data = QuizSchema(**parsed_data).model_dump()
                return validate_quiz_logic(quiz_data)

        except Exception as error:
            print(f"Gemini Versuch {attempt + 1} fehlgeschlagen: {error}")

            if attempt < 4:
                wait_time = get_retry_wait_time(attempt)
                print(f"Warte {wait_time} Sekunden bis zum nächsten Versuch...")
                time.sleep(wait_time)

    print("Gemini nicht verfügbar, Dummy-Quiz wird verwendet.")
    return build_dummy_quiz()


