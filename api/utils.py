import os
from django.conf import settings
from google import genai
from typing import List
from pydantic import BaseModel
import pymupdf
import re


def extract_text_from_pdf(filename):
    doc = pymupdf.open(filename)
    return clean_text('\n'.join([page.get_text() for page in doc]))


def clean_text(text):
    # Patterns for emails and phone numbers
    email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
    phone_pattern = r'\+?\d[\d\s\-\(\)]{8,}\d'

    # Extract emails and phone numbers
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    # Replace emails and phone numbers with placeholders
    for i, email in enumerate(emails):
        text = text.replace(email, f'__EMAIL_{i}__')

    for i, phone in enumerate(phones):
        text = text.replace(phone, f'__PHONE_{i}__')

    # Remove newlines
    text = re.sub(r'\r?\n', ' ', text)

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

    # Remove unwanted characters (you can tweak this to allow some punctuation if needed)
    text = re.sub(r'[^\w\s]', ' ', text)

    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Restore emails and phone numbers
    for i, email in enumerate(emails):
        text = text.replace(f'__EMAIL_{i}__', email)

    for i, phone in enumerate(phones):
        text = text.replace(f'__PHONE_{i}__', phone)

    return text

class ATSAnalysis(BaseModel):
    ats_score: int
    cv_skills: List[str]
    required_skills: List[str]
    improvements: list[str]


def get_ats_score(job_description, resume_text):
    sys_instruct = """
    You are an AI designed to evaluate resumes for job descriptions. Given the following input, return the following information in JSON format:
    
    1. **Matching Percentage**: A percentage value representing how well the resume matches the job description.
    2. **Detected Skills**: A list of skills detected in the resume.
    3. **Required Skills**: A list of skills required by the job description.
    4. **Suggested Improvements**: Suggestions for improving the resume to better match the job description.
    
     Return the response in valid JSON format following this schema:
    {
    "ats_score": int,
        "cv_skills": list[str],
        "required_skills": list[str],
        "improvements": list[str]
    }
    """
    prompt = f"""
    **CV Text:**
    {resume_text}

    **Job Description:**
    {job_description}
    """
    ats_data = {
        "matching_percentage": None,
        "detected_skills": [],
        "required_skills": [],
        "suggested_improvements": []
    }

    try:
        client = genai.Client(api_key="AIzaSyB9cJ5PLtWVP4N5g_uuEgnyj7nDzW_Ecfo")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                'response_mime_type': 'application/json',
                'response_schema': ATSAnalysis,
            },
            contents=prompt,
        )
        response_data = response.text
        print(f"Printed: {response_data}")

        ats_result: ATSAnalysis = response.parsed
        return ats_result

    except Exception as e:
        print(f"Error during API request or response parsing: {e}")
        return None

def process_cv_and_job_description():
    cv_path = os.path.join(settings.MEDIA_ROOT, 'cv.pdf')
    job_desc_path = os.path.join(settings.MEDIA_ROOT, 'job_description.txt')

    if os.path.exists(cv_path) and os.path.exists(job_desc_path):
        resume_text = extract_text_from_pdf(cv_path)
        
        with open(job_desc_path, 'r', encoding='utf-8') as file:
            job_description = file.read()

        ats_result = get_ats_score(job_description, resume_text)

        if ats_result:
            result_data = ats_result.model_dump()
        else:
            result_data = {
                "ats_score": 0,
                "cv_skills": [],
                "required_skills": [],
                "improvements": []
            }

    return result_data