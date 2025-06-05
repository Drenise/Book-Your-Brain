
# quiz_app.py

import streamlit as st
import PyPDF2
import docx
import random
import json
import os

# ---------------------- Helper Functions ---------------------- #
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def split_into_units(text):
    # Basic splitter by heading (tune this as needed)
    units = text.split("Unit")
    return [u.strip() for u in units if u.strip()]

def generate_quiz_questions(unit_text, num_questions=74):
    # Simple question generator from sentences
    sentences = unit_text.split(".")
    questions = []
    for _ in range(num_questions):
        sentence = random.choice(sentences).strip()
        if len(sentence.split()) < 5:
            continue
        words = sentence.split()
        index = random.randint(0, len(words)-1)
        answer = words[index]
        words[index] = "_____"
        question = " ".join(words)
        questions.append({"question": question, "answer": answer, "marks": 2})  # 2 marks each => 74*2=148, adjust if needed
    return questions

def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            return json.load(f)
    else:
        return []

def save_history(history):
    with open("history.json", "w") as f:
        json.dump(history, f)

# ---------------------- Streamlit App ---------------------- #
st.set_page_config(page_title="🧠 Futuristic Quiz App", layout="wide")

st.title("🚀 Starving for Knowledge! 📚")
st.subheader("Upload your educational file and start your journey towards 150 Knowledge Bucks per unit!")

uploaded_file = st.file_uploader("Upload your Word (.docx) or PDF file", type=["docx", "pdf"])
if uploaded_file:
    if uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in pdf_reader.pages])

    units = split_into_units(text)

    st.sidebar.title("📖 Units/Topics")
    unit_options = [f"Unit {i+1}" for i in range(len(units))]
    selected_unit = st.sidebar.selectbox("Select Unit/Topic", unit_options)

    unit_index = int(selected_unit.split()[1]) - 1
    unit_text = units[unit_index]

    # Skip option
    if st.sidebar.button("Skip this Quiz"):
        st.warning("Quiz skipped! Select another unit to continue.")
    else:
        st.header(f"Quiz for {selected_unit} (150 Marks)")

        questions = generate_quiz_questions(unit_text, num_questions=74)
        total_score = 0

        for idx, q in enumerate(questions):
            user_answer = st.text_input(f"Q{idx+1}: {q['question']}")
            if user_answer:
                if user_answer.strip().lower() == q['answer'].strip().lower():
                    st.success(f"✅ Correct! +{q['marks']} Knowledge Bucks 💰")
                    total_score += q['marks']
                else:
                    st.error(f"❌ Incorrect. The correct answer was: {q['answer']}")

        st.markdown("---")
        st.info(f"🎉 Total Score: {total_score} / 150 Knowledge Bucks 💸")

        # Save history
        history = load_history()
        history.append({"unit": selected_unit, "score": total_score})
        save_history(history)

        # WhatsApp share button
        share_text = f"I just scored {total_score} Knowledge Bucks in {selected_unit}! Try it yourself! 🚀📚"
        whatsapp_link = f"https://wa.me/?text={share_text.replace(' ', '%20')}"
        st.markdown(f"[📱 Share on WhatsApp]({whatsapp_link})")

    # History page
    st.sidebar.markdown("---")
    if st.sidebar.button("📜 View Quiz History"):
        history = load_history()
        st.sidebar.header("🏆 Quiz History")
        for record in history:
            st.sidebar.markdown(f"• **{record['unit']}**: {record['score']} Knowledge Bucks 💸")

else:
    st.info("Please upload a file to get started.")
