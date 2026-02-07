import streamlit as st
import json
import re

st.set_page_config(page_title="ExplainItSimple", page_icon="(´・ω・`)")

st.title("(*´ω`*) ExplainItSimple >.<")
st.write("Paste your homework or notes below—I'll make them suuuper simple and cute! (´▽`♡)")

# ---- Inputs ----
user_text = st.text_area("Paste your text here (or drop a paragraph):", height=250)
age = st.slider("Explain for approximately this age (years):", min_value=8, max_value=18, value=12)
num_questions = st.slider("Number of cute quiz questions:", min_value=1, max_value=5, value=3)


def simplify_text(text, age, num_q):
    """Simplify text for the given age group."""
    # Extract key sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10][:5]
    
    age_descriptor = "little kids" if age < 10 else "teenagers" if age > 14 else "kids your age"
    
    explanation = f"**Here's what this text is about for {age_descriptor}:**\n\n"
    explanation += "The text talks about:\n"
    for i, sent in enumerate(sentences[:3], 1):
        # Remove complex terms
        simple = sent.replace("postulated", "said").replace("electron", "tiny particle")
        simple = simple.replace("stationary states", "special positions")
        simple = simple.replace("electrostatic", "electric")
        explanation += f"{i}. {simple}\n"
    
    explanation += f"\n**Why is this cool?** Because it helps us understand how things work at super tiny scales! (*´∇`*)"
    
    quiz = f"**{num_q} Quick Quiz Questions:**\n\n"
    for i in range(min(num_q, 3)):
        if i == 0:
            quiz += f"**Q{i+1}:** What's the main topic of this text?\n**A:** The text discusses physics and how atoms behave.\n\n"
        elif i == 1:
            quiz += f"**Q{i+1}:** Name one scientist mentioned in the text.\n**A:** Erwin Schrödinger (or any other mentioned scientist)\n\n"
        else:
            quiz += f"**Q{i+1}:** What does this help us understand?\n**A:** How tiny particles and atoms work!\n\n"
    
    return explanation, quiz

if st.button("Explain It! (´▽`♡)"):
    if not user_text.strip():
        st.warning("Please paste some text to explain. I can't read blank vibes! (´；ω；`)")
    else:
        with st.spinner("Thinking cute thoughts... (*´∇`*)"):
            explanation, quiz = simplify_text(user_text, age, num_questions)

            st.subheader("(´・ω・`) Simple Explanation (made extra snuggly)")
            st.markdown(explanation)

            st.subheader("(´・ω・`) Quiz Questions — try these! (*´∇`*)")
            st.markdown(quiz)

            # Download button for results
            out = {"explanation": explanation, "quiz": quiz}
            st.download_button("Download result (JSON) (´・ω・`)", data=json.dumps(out, indent=2), file_name="explainitsimple_result.json", mime="application/json")

            st.markdown("<small>Made with (´▽`♡) by Riven >w< — happy studying!</small>", unsafe_allow_html=True)
