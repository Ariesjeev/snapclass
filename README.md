<div align="center">

# 📸 SnapClass

### Making attendance faster using AI

Face recognition and voice biometrics that turn a single class photo (or a quick roll-call) into an attendance record.

[**Live App**](https://snapclasses-ai.streamlit.app/) · [**Landing Page**](https://snapclass-frontend-beryl.vercel.app/) · [**Frontend Repo**](https://github.com/Ariesjeev/snapclass-frontend)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?logo=supabase&logoColor=white)
![dlib](https://img.shields.io/badge/dlib-Face%20Recognition-0A66C2)

</div>

---

## 📖 Overview

Taking attendance by hand eats into class time and is easy to get wrong or fake. **SnapClass** is an AI-powered attendance system where a teacher snaps one or more photos of the classroom, and the app identifies every enrolled student by face. For a different flow, students can say "Present" one by one and the app matches each voice against stored voice embeddings.

Teachers create a subject, share a QR code or join link, and students enroll themselves, registering their face (and optionally their voice) once. From there, attendance is a few clicks, with a review step before anything is saved.

## ✨ Features

**For teachers**
- 🔐 Secure registration and login (passwords hashed with `bcrypt`)
- 📧 **Account recovery by email**: forgot your password? Enter your email and get a reset link in your inbox to set a new one. Forgot your username? Enter your email and get it sent to you
- 📚 Create and manage subjects, each with a unique subject code
- 📱 Share a join link or **QR code** so students enroll in seconds
- 📸 **FaceID attendance**: upload one or more class photos and run face analysis
- 🎙️ **Voice attendance**: students speak in sequence and are matched by voice embedding
- ✅ Review the detected attendance report, then confirm and save (or discard)
- 🗂️ Attendance records per subject, with confidence scores and CSV export

**For students**
- 🔗 One-click enrollment through a QR code or join link (auto-enroll after login)
- 🙂 Login with password or **FaceID**
- 🎤 Optional voice enrollment during registration
- 📊 Personal dashboard showing enrolled subjects and attendance

## 🎬 How It Works

```
Teacher creates subject ──► Shares QR / join link ──► Students enroll + register face (and voice)
                                                                    │
Teacher takes class photo(s) or runs voice roll-call ◄──────────────┘
        │
        ▼
Face / voice matched against stored embeddings
        │
        ▼
Teacher reviews report ──► Confirm & save ──► Records stored in Supabase
```

### 🔑 Account Recovery Flow

```
Teacher clicks "Forgot password" ──► Enters registered email ──► Reset link sent to inbox
        │                                                              │
        └──────────────► Opens link ──► Sets a new password ◄──────────┘

Teacher clicks "Forgot username" ──► Enters registered email ──► Username sent to inbox
```

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| App framework | [Streamlit](https://streamlit.io/) |
| Face recognition | `face_recognition`, `dlib` |
| Voice biometrics | `Resemblyzer`, `librosa` |
| Database & auth storage | [Supabase](https://supabase.com/) (PostgreSQL) |
| Security | `bcrypt` |
| Enrollment QR codes | `segno` |
| Data & ML utilities | `numpy`, `pandas`, `scikit-learn`, `Pillow` |
| Landing page | Flask, deployed on Vercel ([separate repo](https://github.com/Ariesjeev/snapclass-frontend)) |

## 📁 Project Structure

```
snapclass/
├── app.py               # Entry point: routing between home, teacher and student screens
├── requirements.txt     # Python dependencies
└── src/
    ├── components/      # Reusable UI pieces (e.g. auto-enroll dialog)
    ├── database/        # Supabase connection and data access
    ├── pipelines/       # Face recognition and voice processing pipelines
    ├── screens/         # Home, teacher and student screens
    ├── services/        # Business logic (auth, account recovery, etc.)
    └── ui/              # Shared styling and UI helpers
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com/) project
- A webcam and microphone (for FaceID login and voice enrollment)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Ariesjeev/snapclass.git
cd snapclass

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Add your Supabase credentials in `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "your-project-url"
SUPABASE_KEY = "your-anon-or-service-key"
# Public URL where the running Streamlit app can receive the recovery link.
APP_URL = "http://localhost:8501"

# Gmail SMTP: use a Google App Password, not your normal Gmail password.
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-gmail-address@gmail.com"
SMTP_PASSWORD = "your-16-character-app-password"
SMTP_FROM = "SnapClass <your-gmail-address@gmail.com>"

```

> Make sure your Supabase tables match what the app expects (teachers, students, subjects, enrollments and attendance logs).

### Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 🖥️ Usage

1. **Teacher:** register, log in, and create a subject from **Manage Subjects**.
2. Click **Share Class Link** and send the QR code or link to students.
3. **Students:** open the link, register (face plus optional voice), and enroll.
4. **Teacher:** open **Take Attendance**, pick a subject, add class photos and run **Face Analysis**, or use **Voice Attendance**.
5. Review the attendance report and **Confirm & Save**.
6. Check history any time under **Attendance Records**.

**Forgot your login details? (teachers)**
- **Forgot password:** click *Forgot password*, enter your registered email, open the reset link sent to your inbox, and set a new password.
- **Forgot username:** click *Forgot username*, enter your registered email, and your username is sent to you.

## 🗺️ Roadmap

- [ ] Liveness detection to block photo spoofing
- [ ] Per-student attendance analytics and low-attendance alerts
- [ ] Bulk CSV export across subjects
- [ ] Docker setup for easier local install

## 🙏 Acknowledgements

This project was built while following the SnapClass tutorial by **Apna College**, then extended and deployed on my own. Face recognition is powered by [`face_recognition`](https://github.com/ageitgey/face_recognition) and voice embeddings by [`Resemblyzer`](https://github.com/resemble-ai/Resemblyzer).

## 👤 Author

**Jeevan Bikash Sahoo**: Full Stack Developer & AI Engineer
GitHub: [@Ariesjeev](https://github.com/Ariesjeev)

---

<div align="center">If you found this useful, consider giving it a ⭐</div>
