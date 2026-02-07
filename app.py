import streamlit as st
import json
import re
import requests

st.set_page_config(page_title="ExplainItSimple", page_icon="(´・ω・`)")

st.title("(*´ω`*) ExplainItSimple >.<")
st.write("Paste your homework or notes below—I'll make them suuuper simple and cute! (´▽`♡)")

# ---- Inputs ----
user_text = st.text_area("Paste your text here (or drop a paragraph):", height=250)
age = st.slider("Explain for approximately this age (years):", min_value=8, max_value=18, value=12)
num_questions = st.slider("Number of cute quiz questions:", min_value=1, max_value=5, value=3)

# Mode: lightweight or hosted model
mode = st.radio("Mode:", ("Lightweight (no API)", "Hosted LLM (requires API key)"), index=0)
api_provider = None
api_key = None
model_name = None
if mode.startswith("Hosted"):
    api_provider = st.selectbox("Provider:", ("HuggingFace", "OpenAI"))
    # sensible defaults per provider
    default_model = "google/flan-t5-small" if api_provider == "HuggingFace" else "gpt-3.5-turbo"
    model_name = st.text_input("Model name:", value=default_model)
    api_key = st.text_input("API key (kept local):", type="password")
    st.info("API keys must be provided here or via environment variables on deployment. Do NOT commit secrets.")


def simplify_text(text, age, num_q):
    """Simplify text with engaging commentary for the given age group."""
    # Extract key sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15][:8]
    
    age_descriptor = "little kids" if age < 10 else "teenagers" if age > 14 else "kids your age"
    
    # Detect topic from text
    text_lower = text.lower()
    if "percent" in text_lower or "composition" in text_lower:
        topic = "percent composition and identifying compounds"
        why_care = "Understanding percent composition helps chemists identify unknown substances and make new materials! It's like figuring out a recipe by knowing the exact amounts of each ingredient."
    elif "empirical" in text_lower or "formula" in text_lower:
        topic = "chemical formulas and their ratios"
        why_care = "Knowing how to work with empirical and molecular formulas lets scientists understand what chemicals are actually made of and predict how they'll behave!"
    elif "schrodinger" in text_lower or "quantum" in text_lower or "electron" in text_lower:
        topic = "quantum mechanics and atomic behavior"
        why_care = "This explains how the universe works at the tiniest level and is the foundation of ALL modern technology!"
    elif "water" in text_lower or "h2o" in text_lower:
        topic = "the properties and composition of water"
        why_care = "Water is literally essential for life, so understanding its composition and properties is super important!"
    else:
        topic = "this topic"
        why_care = "This knowledge helps you understand the world better and can be applied in tons of real-world situations!"
    
    # More engaging intro with commentary
    explanation = f"✨ **Alright bestie, let me break this down for you!** ✨\n\n"
    explanation += f"So you're learning about {topic} (´・ω・`), and I'm gonna make it super easy to understand!\n\n"
    
    explanation += "**Here's the main tea:**\n\n"
    
    # Add engaging commentary for each key point
    commentary = [
        "**The Big Picture:** ",
        "**Deep Dive Moment:** ",
        "**Real World Connection:** "
    ]
    
    for i, sent in enumerate(sentences[:3], 1):
        # Remove complex chemistry terms
        simple = sent.replace("percent composition", "how much of each element is in something")
        simple = simple.replace("empirical formula", "the simplest ratio of atoms")
        simple = simple.replace("molecular formula", "the actual number of atoms in a molecule")
        simple = simple.replace("molar mass", "how heavy one mole of something is")
        simple = simple.replace("mole", "a counting unit for super tiny particles")
        simple = simple.replace("postulated", "said").replace("electron", "tiny particle")
        simple = simple.replace("stationary states", "special allowed positions")
        simple = simple.replace("electrostatic", "electric").replace("quantum", "super tiny-scale")
        simple = simple.replace("mechanics", "rules of nature").replace("atom", "teeny tiny thing")
        
        # Add engaging commentary
        comment = commentary[i-1] if i <= len(commentary) else f"**Fun Fact #{i}:** "
        explanation += f"{comment} {simple}\n\n"
    
    explanation += "**Why Should You Care?** (´▽`♡)\n"
    explanation += f"{why_care} Plus, mastering this stuff makes you super smart! (*´∇`*)\n"
    
    quiz = f"\n\n**{num_q} Super Engaging Quiz Questions:**\n\n"
    
    # Detect topic to customize quiz
    if "percent" in text_lower or "composition" in text_lower:
        questions = [
            ("What Is It?", "(´・ω・`)", "What does 'percent composition' actually mean?", "It's how much each element contributes to the total mass of a compound!"),
            ("Show Your Work", "(*´ω`*)", "How do you calculate percent composition?", "Divide the mass of each element by the total molar mass, then multiply by 100!"),
            ("Why It Matters", "(´▽`♡)", "Why is finding percent composition useful in chemistry?", "It helps scientists identify unknown compounds and figure out what they're made of!"),
            ("Real Example", "(*´∇`*)", "In water (H₂O), which element has a bigger percent composition?", "Oxygen! It's about 88.8% while hydrogen is only 11.2% by mass!"),
            ("Challenge Mode", "(´；ω；`)", "What's the difference between percent composition and empirical formula?", "Percent composition tells you the percentages by mass, while empirical formula shows the ratio of atoms!"),
        ]
    elif "empirical" in text_lower or "formula" in text_lower:
        questions = [
            ("What Is It?", "(´・ω・`)", "What's an empirical formula?", "It's the simplest ratio of atoms in a compound (but NOT the actual number of atoms)!"),
            ("Show Your Work", "(*´ω`*)", "How do you find an empirical formula from percent composition?", "Assume 100g, convert to moles, divide by the smallest number to get the ratio!"),
            ("Why It Matters", "(´▽`♡)", "Why can two different compounds have the same empirical formula?", "Because NO₂ and N₂O₄ both have the same atom ratio (1:2) even though they're different!"),
            ("Real Example", "(*´∇`*)", "What does an empirical formula tell you that a molecular formula doesn't?", "The empirical formula shows the ratio, but not the exact number of atoms in the molecule!"),
            ("Challenge Mode", "(´；ω；`)", "How do you convert an empirical formula to a molecular formula?", "Find the molar mass of the empirical formula, then divide the compound's molar mass by that!"),
        ]
    else:
        questions = [
            ("Main Topic", "(´・ω・`)", "What's the main topic of this text?", "The text covers key concepts that help you understand this subject better!"),
            ("Key Details", "(*´ω`*)", "Can you identify one important detail from what you just read?", "Yes! The text explains important relationships and how things connect!"),
            ("Why Learn It?", "(´▽`♡)", "Why is this information useful in real life?", "Understanding these concepts helps solve real-world problems and make better decisions!"),
            ("Deep Thinking", "(*´∇`*)", "How does this connect to other things you've learned?", "These concepts build on each other to create a complete picture of the topic!"),
            ("Challenge Mode", "(´；ω；`)", "Can you think of a way to apply what you just learned?", "Try explaining it to a friend or thinking of real-world examples!"),
        ]
    
    for i in range(min(num_q, len(questions))):
        title, emote, question, answer = questions[i]
        quiz += f"**Q{i+1}: {title}** {emote}\n{question}\n**A:** {answer}\n\n"
    
    return explanation, quiz


def call_hosted(prompt, provider, api_key, model="gpt-3.5-turbo"):
    """Call a hosted LLM provider (HuggingFace or OpenAI) via HTTP. Returns string or None on error."""
    try:
        if provider == "HuggingFace":
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": 400, "temperature": 0.2}}
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text") or str(data[0])
            if isinstance(data, dict) and data.get("generated_text"):
                return data.get("generated_text")
            return str(data)

        if provider == "OpenAI":
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            body = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 500,
            }
            resp = requests.post(url, headers=headers, json=body, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

        return None
    except Exception as e:
        st.error(f"Hosted API error: {str(e)[:200]}")
        return None

if st.button("Explain It! (´▽`♡)"):
    if not user_text.strip():
        st.warning("Please paste some text to explain. I can't read blank vibes! (´；ω；`)")
    else:
        with st.spinner("Thinking cute thoughts... (*´∇`*)"):
            explanation = None
            quiz = None

            if mode.startswith("Hosted"):
                if not api_key:
                    st.warning("Hosted LLM selected — please enter your API key above.")
                    st.stop()

                prompt = (
                    f"Explain this text simply for a {age}-year-old and then produce {num_questions} short quiz questions."
                    "\n\nLABEL THE RESPONSE WITH 'EXPLANATION' THEN 'QUIZ' SO IT'S EASY TO PARSE.\n\n"
                    f"TEXT:\n{user_text}"
                )

                hosted_out = call_hosted(prompt, api_provider, api_key, model_name)
                if not hosted_out:
                    st.error("Hosted model returned no output.")
                    st.stop()

                # Try to split hosted output by markers
                if "EXPLANATION" in hosted_out:
                    explanation = hosted_out.split("EXPLANATION")[-1]
                    explanation = explanation.split("QUIZ")[0].strip()
                else:
                    explanation = hosted_out[:800]

                if "QUIZ" in hosted_out:
                    quiz = hosted_out.split("QUIZ")[-1].strip()
                else:
                    # fallback: generate quiz from the original text
                    _, quiz = simplify_text(user_text, age, num_questions)

            else:
                explanation, quiz = simplify_text(user_text, age, num_questions)

            st.subheader("(´・ω・`) Simple Explanation (made extra snuggly)")
            st.markdown(explanation)

            st.subheader("(´・ω・`) Quiz Questions — try these! (*´∇`*)")
            st.markdown(quiz)

            # Download button for results
            out = {"explanation": explanation, "quiz": quiz}
            st.download_button("Download result (JSON) (´・ω・`)", data=json.dumps(out, indent=2), file_name="explainitsimple_result.json", mime="application/json")

            st.markdown("<small>Made with (´▽`♡) by Riven >w< — happy studying!</small>", unsafe_allow_html=True)
