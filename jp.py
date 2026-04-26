import streamlit as st
import random
import json
import os

st.set_page_config(page_title="JLPT Practice App", layout="centered")

st.title("🇯🇵 JLPT Practice App")

# 📚 Lessons data
lessons = {
    "Lesson 1": [
        {"question": "I (polite)", "jp": "わたし", "en": "watashi"},
        {"question": "That person (polite)", "jp": "あのかた", "en": "ano kata"},
        {"question": "Student", "jp": "がくせい", "en": "gakusei"},
        {"question": "Teacher", "jp": "せんせい", "en": "sensei"},
        {"question": "Company employee", "jp": "かいしゃいん", "en": "kaishain"},
    ]
}

# 📌 Sidebar
lesson_choice = st.sidebar.selectbox("Select Lesson", list(lessons.keys()))

# 🔀 Randomize toggle
shuffle = st.sidebar.toggle("🔀 Randomize Questions")

# 📂 Score file
SCORE_FILE = "scores.json"

# Load scores
if os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "r") as f:
        scores_data = json.load(f)
else:
    scores_data = {}

questions = lessons[lesson_choice].copy()

# 🔀 Shuffle INSIDE quiz
if shuffle:
    random.shuffle(questions)

st.header(f"📝 {lesson_choice} Test")

user_answers = []
score = 0

# 🧪 Questions
for i, q in enumerate(questions):
    user_input = st.text_input(f"{i+1}. {q['question']}", key=f"{lesson_choice}_{i}")
    user_answers.append(user_input.strip().lower())

# ✅ Submit
if st.button("Submit"):
    st.subheader("📊 Results")

    for i, q in enumerate(questions):
        if user_answers[i] in [q["jp"], q["en"]]:
            st.success(f"{i+1}. Correct ✅")
            score += 1
        else:
            st.error(f"{i+1}. Wrong ❌ (JP: {q['jp']} | EN: {q['en']})")

    st.write(f"## 🎯 Score: {score}/{len(questions)}")

    # 🏆 Save score
    if lesson_choice not in scores_data:
        scores_data[lesson_choice] = []

    scores_data[lesson_choice].append(score)

    with open(SCORE_FILE, "w") as f:
        json.dump(scores_data, f)

# 🏆 Scoreboard
st.sidebar.subheader("🏆 Scoreboard")

if lesson_choice in scores_data:
    st.sidebar.write(f"Scores for {lesson_choice}:")
    st.sidebar.write(scores_data[lesson_choice])

    # Show best score
    best = max(scores_data[lesson_choice])
    st.sidebar.write(f"🔥 Best: {best}")
else:
    st.sidebar.write("No scores yet")