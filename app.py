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
    """Simplify text with engaging commentary for the given age group."""
    # Extract key sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10][:6]
    
    age_descriptor = "little kids" if age < 10 else "teenagers" if age > 14 else "kids your age"
    
    # More engaging intro with commentary
    explanation = f"✨ **Alright bestie, let me break this down for you!** ✨\n\n"
    explanation += f"So you're learning about some pretty advanced stuff here (´・ω・`), and I'm gonna make it super easy to understand!\n\n"
    
    explanation += "**Here's the main tea:**\n\n"
    
    # Add engaging commentary for each key point
    commentary = [
        "**The Big Picture:** ",
        "**Deep Dive Moment:** ",
        "**Plot Twist Alert:** "
    ]
    
    for i, sent in enumerate(sentences[:3], 1):
        # Remove complex terms
        simple = sent.replace("postulated", "said").replace("electron", "tiny particle")
        simple = simple.replace("stationary states", "special positions")
        simple = simple.replace("electrostatic", "electric").replace("quantum", "super tiny")
        simple = simple.replace("mechanics", "rules of nature").replace("atom", "teeny tiny thing")
        
        # Add engaging commentary
        comment = commentary[i-1] if i <= len(commentary) else f"**Fun Fact #{i}:** "
        explanation += f"{comment} {simple}\n\n"
    
    explanation += "**Why Should You Care?** (´▽`♡)\n"
    explanation += "This stuff explains how the universe works at the tiniest level! Scientists like Schrödinger figured out that tiny particles don't follow the same rules as big stuff—it's wild! Understanding this is like having a superpower to see how atoms behave. Plus, this is the foundation of literally ALL modern technology (phones, computers, everything!). Isn't that insane?? (*´∇`*)\n"
    
    quiz = f"\n\n**{num_q} Super Engaging Quiz Questions:**\n\n"
    
    # Quiz question templates with emotes
    questions = [
        ("The Main Idea", "(´・ω・`)", "What's the BIG topic of this text?", "Scientists explaining how atoms and tiny particles work, especially the revolutionary ideas from Schrödinger!"),
        ("Name Dropping", "(*´ω`*)", "Who was one of the MAJOR scientists mentioned that changed physics forever?", "Erwin Schrödinger (or Albert Einstein, Niels Bohr—they're all legends!)"),
        ("Why It Matters", "(´▽`♡)", "What does understanding quantum mechanics help us do?", "Build technology, understand the universe, and appreciate how absolutely BONKERS reality is at tiny scales!"),
        ("Deep Concepts", "(*´∇`*)", "Can you explain what 'stationary states' means in simple terms?", "They're special positions where electrons can exist without losing energy—like special allowed seats in a theater!"),
        ("Super Challenge", "(´；ω；`)", "How did scientists' ideas about atoms change over time?", "They went from thinking atoms were solid balls → mini solar systems → wave-like probability clouds. Mind = BLOWN!")
    ]
    
    for i in range(min(num_q, len(questions))):
        title, emote, question, answer = questions[i]
        quiz += f"**Q{i+1}: {title}** {emote}\n{question}\n**A:** {answer}\n\n"
    
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
