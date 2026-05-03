# Quizliy Backend

## 📌 Overview

Quizliy is a Django REST backend that generates quizzes from YouTube videos using AI.

Flow:

YouTube URL → Audio Extraction → Transcription → AI Quiz Generation → Stored Quiz → Frontend Display

---

## 🚀 Features

- User registration & login (JWT via HTTP-only cookies)
- Create quizzes from YouTube URLs
- Automatic transcription using Whisper
- AI-generated quizzes using Gemini API
- Automatic fallback to dummy quiz if AI fails
- View, update, and delete quizzes

---

## 🛠️ Tech Stack

- Python (Django, Django REST Framework)
- JWT Authentication (SimpleJWT + HTTP-only cookies)
- yt-dlp (Audio extraction)
- Whisper (Speech-to-text)
- Gemini API (AI quiz generation)
- SQLite (Database)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd quizliy_backend
````

### 2. Create virtual environment

```bash
python -m venv env
source env/Scripts/activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

---

### ⚠️ Requirements

You must install **FFmpeg globally** for audio processing:

Download:
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Check installation:

```bash
ffmpeg -version
```

---

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Start server

```bash
python manage.py runserver
```

---

## 🔑 Authentication

Authentication is handled using JWT stored in HTTP-only cookies.

Tokens are stored in HTTP-only cookies to improve security and prevent XSS attacks.

### Endpoints

| Method | Endpoint            | Description   |
| ------ | ------------------- | ------------- |
| POST   | /api/register/      | Register user |
| POST   | /api/login/         | Login user    |
| POST   | /api/logout/        | Logout user   |
| POST   | /api/token/refresh/ | Refresh token |

---

## 📊 Quiz Endpoints

| Method | Endpoint           | Description          |
| ------ | ------------------ | -------------------- |
| GET    | /api/quizzes/      | Get all user quizzes |
| POST   | /api/quizzes/      | Create new quiz      |
| GET    | /api/quizzes/{id}/ | Get single quiz      |
| PATCH  | /api/quizzes/{id}/ | Update quiz          |
| DELETE | /api/quizzes/{id}/ | Delete quiz          |

---

## 🤖 AI Integration

The system uses the Gemini API to generate quizzes from transcripts.

### Fallback Logic

If the Gemini API fails (e.g. quota exceeded), the system automatically generates a dummy quiz.

This ensures the application remains fully functional even without AI availability.

---

## 🧪 Testing

The API can be tested using Postman.

Recommended test flow:

1. Register a user
2. Login
3. Create a quiz using a YouTube URL
4. Fetch quizzes
5. Update a quiz
6. Delete a quiz
7. Logout

---

## 🧠 Architecture

The project follows a service-based structure:

* Views handle HTTP requests and responses
* Services contain business logic (AI, transcription, processing)
* Models define database structure

This separation improves maintainability and scalability.

---

## 📁 Project Structure

```
quizliy_backend/
│
├── authentication/
├── quizzes/
├── core/
├── media/
├── manage.py
└── .env
```

---

## ⚠️ Notes

* Gemini API has usage limits (quota)
* Dummy quiz fallback ensures stability
* FFmpeg is required for audio processing
* Whisper runs locally and may take time depending on hardware

---

## 📌 Status

* Backend: ✅ Completed
* Authentication: ✅ Working
* Quiz generation: ✅ Working (with fallback)
* API: ✅ Fully functional

---

## 👨‍💻 Author

Yunus – Junior Software Developer
Project built during Developer Akademie training
