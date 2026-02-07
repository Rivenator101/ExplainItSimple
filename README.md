Project Name: ExplainItSimple
Date: Feb 7, 2026

Name and School: Liz - [Your School]

Description:
ExplainItSimple is an AI-powered tool that converts complex academic text into simple explanations targeted at a chosen age, and generates short quiz questions to aid studying and retention.

How to run locally:
1. Create a virtual environment (recommended).
2. Install dependencies:

   pip install -r requirements.txt

3. Run the app:

   streamlit run app.py

4. Enter your OpenAI API key in the app and paste text to get a simplified explanation + quiz.

What to include in the GitHub repo for Devpost:
- This README (with names and date)
- All source files in `/src` or root
- Slide deck in `/slides`
- Video link in `/video`

Minimal project checklist (Devpost rules):
- README with names and date (this file)
- Public GitHub repo created today
- Slide deck (upload to `/slides`)
- 1-3 minute demo video link (place in `/video/script.md` or add link)

Notes:
- The app uses OpenAI's ChatCompletion API; change the `MODEL` constant in `app.py` if needed.
- Keep your API key private; do not commit it to the repo.
