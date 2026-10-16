# AI Resume Analyzer & Job Matcher

A Streamlit app that extracts text from PDF resumes, compares resume and
job-description text using TF-IDF and cosine similarity, identifies
potential keyword and skill gaps, and optionally generates suggestions
using Google Gemini.

## Features
- PDF resume text extraction
- TF-IDF and cosine similarity score
- Recognized skill and keyword comparison
- Optional Gemini suggestions for summary, skills and project bullets
- Input validation and readable error messages

## Local setup
1. Create and activate a virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` if using Gemini and add your API key.
4. Run `python -m streamlit run app.py`.

## Gemini configuration
Set `GEMINI_API_KEY` in `.env`. Never commit `.env` or share the API key.

The similarity score is not a hiring probability or an official ATS score.
Keyword presence does not prove a candidate's proficiency.
