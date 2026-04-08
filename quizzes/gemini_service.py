# MYA: Neu - Gemini Service für Quiz-Generierung

from pydantic import BaseModel, Field, ValidationError
from google import genai


# MYA: Neu - Schema für einzelne Frage
class QuizQuestionSchema(BaseModel):
    question_title: str = Field(min_length=5)
    question_options: list[str] = Field(min_length=4, max_length=4)
    answer: str = Field(min_length=1)


# MYA: Neu - Schema für komplettes Quiz
class QuizSchema(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=150)
    questions: list[QuizQuestionSchema] = Field(min_length=10, max_length=10)


# MYA: Neu - Prompt bauen
def build_quiz_prompt(transcript):
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


# MYA: Neu - zusätzliche Logik validieren
def validate_quiz_logic(data):
    for question in data["questions"]:
        options = question["question_options"]

        if len(options) != 4:
            raise ValueError("Eine Frage hat nicht genau 4 Optionen.")
        if len(set(options)) != 4:
            raise ValueError("Eine Frage enthält doppelte Optionen.")
        if question["answer"] not in options:
            raise ValueError("Antwort ist nicht in den Optionen enthalten.")

    return data


# MYA: Neu - Gemini aufrufen und Ergebnis validieren
def generate_quiz_from_transcript(transcript):
    client = genai.Client()
    prompt = build_quiz_prompt(transcript)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": QuizSchema.model_json_schema(),
        },
    )

    try:
        quiz_data = QuizSchema.model_validate_json(response.text).model_dump()
        return validate_quiz_logic(quiz_data)
    except ValidationError as error:
        raise ValueError(f"Gemini JSON Fehler: {error}") from error