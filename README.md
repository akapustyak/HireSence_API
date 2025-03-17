# Django REST API for CV Analysis

## 📌 Project Overview
This Django REST API allows users to upload a CV (PDF) and a job description (text), then processes them using AI to evaluate the match between the CV and the job description. It returns an ATS score, extracted skills, required skills, and improvement suggestions.

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2️⃣ Create and Activate a Virtual Environment
```sh
python -m venv venv
# Activate venv:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```sh
python manage.py migrate
```

### 5️⃣ Run the Development Server
```sh
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## 🔥 API Endpoints

### 1️⃣ Upload CV (PDF)
**Endpoint:** `POST /api/upload-cv/`
- **Body (multipart/form-data):**
  - `cv` (file) → PDF file of the CV.
- **Response:**
```json
{"message": "CV uploaded successfully"}
```

### 2️⃣ Upload Job Description
**Endpoint:** `POST /api/upload-job-description/`
- **Body (JSON):**
```json
{"job_description": "We are looking for a Python Developer..."}
```
- **Response:**
```json
{"message": "Job description uploaded successfully"}
```

### 3️⃣ Get ATS Score and Suggestions
**Endpoint:** `GET /api/get-result/`
- **Response:**
```json
{
    "ats_score": 75,
    "cv_skills": ["Python", "Django", "Machine Learning"],
    "required_skills": ["Python", "AWS", "Agile"],
    "improvements": ["Mention AWS experience if any.", "State Agile experience explicitly."]
}
```

## 🚀 Additional Notes
- Make sure `MEDIA_ROOT` is correctly set in `settings.py` for file uploads.
- To enable OpenAPI documentation, install `drf-spectacular` and add:
```sh
pip install drf-spectacular
```
Then, add this to `urls.py`:
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```
Now, visit `http://127.0.0.1:8000/api/docs/` for interactive API documentation!

---
