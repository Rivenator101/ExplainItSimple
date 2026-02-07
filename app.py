import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="ExplainItSimple", page_icon="🧠✨")

st.title("🧠✨ ExplainItSimple >.<")
st.write("Paste your homework or notes below—I'll make them suuuper simple and cute! 💖")

# ---- Inputs ----
api_key = None
# Prefer Streamlit secrets, then environment variable, then UI input.
# IMPORTANT: do NOT commit your API key to the repo.
if hasattr(st, "secrets") and st.secrets.get("HUGGINGFACE_API_KEY"):
    api_key = st.secrets.get("HUGGINGFACE_API_KEY")
else:
    api_key = os.getenv("HUGGINGFACE_API_KEY")

if api_key:
    st.info("Using HuggingFace API key from environment/Streamlit secrets. 🔒")
else:
    api_key = st.text_input("Enter your HuggingFace API Key (free at https://huggingface.co/settings/tokens):", type="password")

user_text = st.text_area("Paste your text here (or drop a paragraph):", height=250)
age = st.slider("Explain for approximately this age (years):", min_value=8, max_value=18, value=12)
num_questions = st.slider("Number of cute quiz questions:", min_value=1, max_value=5, value=3)

if not api_key:
    st.info("Enter your HuggingFace API key (free, no age restriction!) to generate explanations. (I promise to be gentle!) 🥺")
    st.stop()

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


def call_openai(prompt, api_key, model="meta-llama/Llama-2-7b-chat-hf", max_tokens=800):
    """Call HuggingFace Inference API."""
    url = f"https://router.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_tokens,
            "temperature": 0.2,
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"HuggingFace API error: {resp.text}")
    result = resp.json()
    # Extract text from response
    if isinstance(result, list) and len(result) > 0:
        if "generated_text" in result[0]:
            return result[0]["generated_text"]
    return str(result)

if st.button("Explain It! 💖"):
    if not user_text.strip():
        st.warning("Please paste some text to explain. I can't read blank vibes! >.<")
    else:
        prompt = build_prompt(user_text, age, num_questions)
        with st.spinner("Thinking cute thoughts... ✨"):
            result = None
            try:
                result = call_openai(prompt, api_key, model="meta-llama/Llama-2-7b-chat-hf", max_tokens=800)
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
                explanation = result[:500]  # Show first 500 chars
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
