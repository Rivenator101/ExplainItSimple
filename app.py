import streamlit as st
import json
import os
from transformers import pipeline

st.set_page_config(page_title="ExplainItSimple", page_icon="🧠✨")

st.title("🧠✨ ExplainItSimple >.<")
st.write("Paste your homework or notes below—I'll make them suuuper simple and cute! 💖")

# ---- Inputs ----
user_text = st.text_area("Paste your text here (or drop a paragraph):", height=250)
age = st.slider("Explain for approximately this age (years):", min_value=8, max_value=18, value=12)
num_questions = st.slider("Number of cute quiz questions:", min_value=1, max_value=5, value=3)

prompt_template = (
    "Explain this text simply for a {age}-year-old:\n\n{input_text}\n\n"
    "EXPLANATION:\n(Clear, friendly explanation in 2-4 short paragraphs)\n\n"
    "QUIZ:\n(Create {n} simple quiz questions with answers)"
)


def build_prompt(text, age, n):
    return prompt_template.format(age=age, n=n, input_text=text)


@st.cache_resource
def load_model():
    """Load the text generation pipeline (cached for performance)."""
    return pipeline("text-generation", model="distilgpt2", device=-1)


def call_openai(prompt, max_tokens=500):
    """Generate text using local distilgpt2 model."""
    try:
        generator = load_model()
        result = generator(prompt, max_length=max_tokens, temperature=0.7, do_sample=True)
        
        if result and len(result) > 0:
            return result[0].get("generated_text", "")
        return ""
    except Exception as e:
        st.error(f"Model Error: {str(e)[:100]} 😿")
        return None

if st.button("Explain It! 💖"):
    if not user_text.strip():
        st.warning("Please paste some text to explain. I can't read blank vibes! >.<")
    else:
        prompt = build_prompt(user_text, age, num_questions)
        with st.spinner("Thinking cute thoughts... ✨"):
            result = None
            try:
                result = call_openai(prompt, max_tokens=500)
            except Exception as e:
                st.error(f"Error: {e} 😵‍💫")
                st.stop()

            # If no result was produced, stop gracefully
            if not result:
                st.stop()

            # Try to split into explanation and quiz if the model followed the format
            st.subheader("📘 Simple Explanation (made extra snuggly)")
            if "EXPLANATION" in result:
                explanation = result.split("EXPLANATION")[-1]
                explanation = explanation.split("QUIZ")[0].strip()
            else:
                # fallback: show first part
                explanation = result[:400]  # Show first 400 chars
            st.markdown(explanation)

            st.subheader("📝 Quiz Questions — try these! ✨")
            if "QUIZ" in result:
                quiz = result.split("QUIZ")[-1].strip()
            else:
                # attempt to find lines that look like questions
                quiz = "\n".join([l for l in result.splitlines() if l.strip()][:10])
            st.markdown(quiz)

            # Download button for results
            out = {"explanation": explanation, "quiz": quiz}
            st.download_button("Download result (JSON) 💾", data=json.dumps(out, indent=2), file_name="explainitsimple_result.json", mime="application/json")

            st.markdown("<small>Made with 💖 by Riven ;3 — happy studying!</small>", unsafe_allow_html=True)
