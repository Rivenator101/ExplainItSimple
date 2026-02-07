import streamlit as st
from openai import OpenAI
import json
import os

st.set_page_config(page_title="ExplainItSimple", page_icon="🧠✨")

st.title("🧠✨ ExplainItSimple >.<")
st.write("Paste your homework or notes below—I'll make them suuuper simple and cute! 💖")

# ---- Inputs ----
api_key = None
# Prefer Streamlit secrets, then environment variable, then UI input.
# IMPORTANT: do NOT commit your API key to the repo.
if hasattr(st, "secrets") and st.secrets.get("OPENAI_API_KEY"):
    api_key = st.secrets.get("OPENAI_API_KEY")
else:
    api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    st.info("Using OpenAI key from environment/Streamlit secrets. 🔒")
else:
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")

user_text = st.text_area("Paste your text here (or drop a paragraph):", height=250)
age = st.slider("Explain for approximately this age (years):", min_value=8, max_value=18, value=12)
num_questions = st.slider("Number of cute quiz questions:", min_value=1, max_value=5, value=3)

MODEL = "gpt-4o-mini"  # preferred model
FALLBACK_MODEL = "gpt-3.5-turbo"  # cheaper fallback if quota errors occur

if not api_key:
    st.info("Enter your OpenAI API key to generate explanations. (I promise to be gentle!) 🥺")
    st.stop()

# Create OpenAI client (newer openai-python interface)
client = OpenAI(api_key=api_key)

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


def demo_mode(user_text, age, num_questions):
    """Return a sample explanation + quiz for demo purposes when API unavailable."""
    sample_explanation = f"""This text discusses important concepts. Here's what you need to know:

- **Key Idea 1:** The main topic is interesting and relevant.
- **Key Idea 2:** There are several supporting details that help explain it.
- **Key Idea 3:** This connects to other knowledge areas.

The main takeaway is that understanding these core ideas will help you with future learning!"""
    
    sample_quiz = f"""**Q1:** What is the main topic?
Answer: The core subject of the text.

**Q2:** Why is this important?
Answer: It helps us understand key concepts.

**Q3:** Can you give a real-world example?
Answer: (Your own answer!)"""
    
    return f"EXPLANATION\n{sample_explanation}\n\nQUIZ\n{sample_quiz}"


def call_openai(prompt, client, model=MODEL, max_tokens=800):
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=max_tokens,
    )

if st.button("Explain It! 💖"):
    if not user_text.strip():
        st.warning("Please paste some text to explain. I can't read blank vibes! >.<")
    else:
        prompt = build_prompt(user_text, age, num_questions)
        with st.spinner("Thinking cute thoughts... ✨"):
            try:
                resp = call_openai(prompt, client, model=MODEL, max_tokens=800)
                # handle a couple of possible response shapes
                try:
                    result = resp["choices"][0]["message"]["content"].strip()
                except Exception:
                    try:
                        result = resp.choices[0].message.content.strip()
                    except Exception:
                        result = str(resp)
            except Exception as e:
                # Detect quota or rate-limit style errors and try a cheaper fallback model
                msg = str(e)
                if "quota" in msg.lower() or "exceeded" in msg.lower() or "insufficient_quota" in msg.lower() or "429" in msg:
                    st.warning("Quota exceeded — using demo mode. (Add billing to OpenAI for live mode.) ⏳")
                    result = demo_mode(user_text, age, num_questions)
                else:
                    # Try fallback model on other errors
                    try:
                        resp = call_openai(prompt, client, model=FALLBACK_MODEL, max_tokens=400)
                        try:
                            result = resp["choices"][0]["message"]["content"].strip()
                        except Exception:
                            try:
                                result = resp.choices[0].message.content.strip()
                            except Exception:
                                result = str(resp)
                    except Exception as e2:
                        st.warning(f"API unavailable — using demo mode to show how ExplainItSimple works. ✨")
                        result = demo_mode(user_text, age, num_questions)

                # If no result was produced (e.g., both preferred and fallback failed), stop gracefully
                if not result:
                    st.error("Something went wrong. Please try again.")
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

            except Exception as e:
                st.error(f"Error: {e} 😵‍💫")
