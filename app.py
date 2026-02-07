import streamlit as st
import google.generativeai as genai
import json
import os

st.set_page_config(page_title="ExplainItSimple", page_icon="🧠✨")

st.title("🧠✨ ExplainItSimple >.<")
st.write("Paste your homework or notes below—I'll make them suuuper simple and cute! 💖")

# ---- Inputs ----
api_key = None
# Prefer Streamlit secrets, then environment variable, then UI input.
# IMPORTANT: do NOT commit your API key to the repo.
if hasattr(st, "secrets") and st.secrets.get("GEMINI_API_KEY"):
    api_key = st.secrets.get("GEMINI_API_KEY")
else:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    st.info("Using Gemini API key from environment/Streamlit secrets. 🔒")
else:
    api_key = st.text_input("Enter your Google Gemini API Key (free at https://makersuite.google.com):", type="password")

user_text = st.text_area("Paste your text here (or drop a paragraph):", height=250)
age = st.slider("Explain for approximately this age (years):", min_value=8, max_value=18, value=12)
num_questions = st.slider("Number of cute quiz questions:", min_value=1, max_value=5, value=3)

if not api_key:
    st.info("Enter your Gemini API key (free!) to generate explanations. (I promise to be gentle!) 🥺")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

prompt_template = (
    "You are an assistant that explains academic text simply and concisely."
    " First, provide a clear, friendly explanation targeted at a {age}-year-old."
    " Then produce {n} short multiple-choice or short-answer quiz questions (Q + A)."
    " Label sections clearly as 'EXPLANATION' and 'QUIZ'. Keep the explanation 2-6 short paragraphs."
    " If the input includes equations or code, keep them but explain them in plain terms.\n\n"
    "TEXT:\n{input_text}"
)


def build_prompt(text, age, n):
    return prompt_template.format(age=age, n=n, input_text=text)


def call_openai(prompt, model="gemini-1.5-flash", max_tokens=800):
    """Call Google Gemini API."""
    model_obj = genai.GenerativeModel(model)
    response = model_obj.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens, temperature=0.2)
    )
    return response.text

if st.button("Explain It! 💖"):
    if not user_text.strip():
        st.warning("Please paste some text to explain. I can't read blank vibes! >.<")
    else:
        prompt = build_prompt(user_text, age, num_questions)
        with st.spinner("Thinking cute thoughts... ✨"):
            result = None
            try:
                result = call_openai(prompt, model="gemini-1.5-flash", max_tokens=1000)
            except Exception as e:
                st.error(f"Error: {e} 😵‍💫")
                st.stop()

            # If no result was produced, stop gracefully
            if not result:
                st.stop()

            # Try to split into explanation and quiz if the assistant followed the format
            st.subheader("📘 Simple Explanation (made extra snuggly)")
            if "EXPLANATION" in result:
                explanation = result.split("EXPLANATION")[-1]
                explanation = explanation.split("QUIZ")[0].strip()
            else:
                # fallback: show first part
                explanation = result
            st.markdown(explanation)

            st.subheader("📝 Quiz Questions — try these! ✨")
            if "QUIZ" in result:
                quiz = result.split("QUIZ")[-1].strip()
            else:
                # attempt to find lines that look like questions
                quiz = "\n".join([l for l in result.splitlines() if l.strip()][:20])
            st.markdown(quiz)

            # Download button for results
            out = {"explanation": explanation, "quiz": quiz}
            st.download_button("Download result (JSON) 💾", data=json.dumps(out, indent=2), file_name="explainitsimple_result.json", mime="application/json")

            st.markdown("<small>Made with 💖 by Riven ;3 — happy studying!</small>", unsafe_allow_html=True)
