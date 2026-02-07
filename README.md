
Project Name: ExplainItSimple
Date: Feb 7, 2026

Name and School: Riven — Iroquois Ridge High School

Overview
--------
ExplainItSimple is a lightweight, student-friendly tool that turns dense academic text into short, age‑targeted explanations and generates a handful of quick quiz questions to help with review and retention. The user picks an age (8–18) and number of quiz questions; the app extracts and simplifies the key ideas and returns a playful, readable summary plus engaging questions.

Run locally
-----------
1. Create and activate a virtual environment (recommended):

   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Run the app locally:

   streamlit run app.py

4. Paste your text into the app and choose the target age and number of quiz questions. No API key is required for the current lightweight mode.

What to include in the GitHub repo (for Devpost)
------------------------------------------------
- This README (with names and date)
- All source files (root or a `src/` folder)
- Slide deck in `/slides`
- Demo video or link in `/video` (or note where the video is hosted)

Minimal Devpost checklist
------------------------
- README with names and date (this file)
- Public GitHub repo
- Slide deck (up to 10 slides) in `/slides`
- 1–3 minute demo video (link in `/video`)

Notes and implementation details
--------------------------------
- The app was implemented with Streamlit and a lightweight text-processing approach to guarantee a fast, reliable demo under tight time constraints. It parses the input, extracts key sentences, simplifies terminology, and produces short, themed quiz questions.
- Earlier iterations explored remote LLM providers (OpenAI, Google Gemini, Hugging Face, Replicate). Due to quota restrictions, age/region limits, and endpoint/dependency issues we pivoted to a local/lightweight approach so the demo would be stable and easy to run.
- Because no API key is required in the final lightweight mode, there is no risk of accidentally committing secrets. If you later switch to an external model (Replicate / HF / OpenAI), keep your API keys in environment variables or platform secrets and never commit them.

Challenges, initial plan, and how we got here
---------------------------------------------
Initial plan
- Quickly prototype a Streamlit front end that uses an LLM to simplify text and produce quizzes. The early plan favored hosted models to maximize explanation quality while keeping UI work minimal.

Key challenges encountered
- OpenAI quota limits: free/quota limits prevented reliable access during rapid demo development.
- Google Gemini: age/region restrictions made it unusable for this user.
- Hugging Face: endpoint changes and authentication differences caused fragile integrations.
- Replicate: worked but required a secret; platform tokens and environment configuration introduced friction.
- Heavy model downloads: trying to run larger local models on Streamlit Cloud caused timeouts and very long dependency installs.

How we solved it (why final approach)
- To meet the hackathon deadline and ensure a working demo, we switched to a robust, no‑secret, no‑heavy-dependency approach: a lightweight in‑app simplifier that reliably summarizes any pasted text and generates contextual quiz questions based on detected keywords.
- This trade-off favors reliability and speed for the live demo while still delivering useful, targeted explanations for students.

License and credits
-------------------
This project was built for the Averix Hacks hackathon (Feb 7, 2026). Feel free to reuse or adapt it for educational purposes 
(With credit). Keep API keys and secrets out of the repo.

Contact
-------
Riven — Iroquois Ridge High School
