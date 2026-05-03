# Quizliy Backend

## 📌 Overview

Quizliy is a full-stack web application that generates quizzes from YouTube videos using AI.

Flow:

YouTube URL → Audio Extraction → Transcription → AI Quiz Generation → Stored Quiz → Frontend Display

---

## 🚀 Features

* User registration & login (JWT via HTTP-only cookies)
* Create quizzes from YouTube URLs
* Automatic transcription using Whisper
* AI-generated quizzes using Gemini API
* Fallback to dummy quiz if AI is unavailable
* View, update, and delete quizzes
* Play quizzes and see results

---

## 🛠️ Tech Stack

* Python (Django, Django REST Framework)
* JWT Authentication (SimpleJWT + Cookies)
* yt-dlp (Audio extraction)
* Whisper (Speech-to-text)
* Gemini API (AI quiz generation)
* SQLite (Database)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd quizliy_backend
```

### 2. Create virtual environment

```bash
python -m venv env
source env/Scripts/activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
GEMINI_API_KEY=your_api_key_here
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

The system uses Gemini API to generate quizzes from transcripts.

### Fallback Logic

If Gemini API fails (e.g. quota exceeded):

```text
Dummy quiz is generated automatically
```

This allows frontend testing without breaking the app.

---

## 🧪 Testing

You can test endpoints using:

* Postman
* Browser (for GET requests)
* Frontend integration

---

## ⚠️ Notes

* Gemini API has usage limits (quota)
* Dummy quiz fallback is active when API fails
* yt-dlp and Whisper must be installed for full functionality

---

## 📁 Project Structure

```text
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

## 📌 Status

* Backend: ✅ Completed
* Authentication: ✅ Working
* Quiz generation: ✅ Working (with fallback)
* Frontend integration: ✅ Working

---

## 👨‍💻 Author

Yunus – Junior Software Developer
Project built during Developer Akademie training
    