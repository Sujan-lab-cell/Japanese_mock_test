import streamlit as st
import random
import os
import csv
import pandas as pd

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

st.header(f"📝 {lesson_choice} Test")

# 🔘 Buttons row (Submit + Randomize)
col1, col2 = st.columns([1, 2])

with col1:
    submit = st.button("Submit")

with col2:
    shuffle = st.checkbox("🔀 Randomize")

# 🎯 Question handling (stable order)
if "questions" not in st.session_state or shuffle:
    q_copy = lessons[lesson_choice].copy()
    if shuffle:
        random.shuffle(q_copy)
    st.session_state.questions = q_copy

questions = st.session_state.questions

# 🧪 Questions
user_answers = []
score = 0

for i, q in enumerate(questions):
    user_input = st.text_input(f"{i+1}. {q['question']}", key=f"{lesson_choice}_{i}")
    user_answers.append(user_input.strip().lower())

# ✅ Submit logic + CSV save
if submit:
    st.subheader("📊 Results")

    for i, q in enumerate(questions):
        if user_answers[i] in [q["jp"], q["en"]]:
            st.success(f"{i+1}. Correct ✅")
            score += 1
        else:
            st.error(f"{i+1}. Wrong ❌ (JP: {q['jp']} | EN: {q['en']})")

    st.write(f"## 🎯 Score: {score}/{len(questions)}")

    # 📂 Save to CSV
    FILE = "scores.csv"
    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Lesson", "Score"])

        writer.writerow([lesson_choice, score])

# 🏆 Scoreboard (CSV based)
st.sidebar.subheader("🏆 Scoreboard")

if os.path.exists("scores.csv"):
    df = pd.read_csv("scores.csv")

    lesson_df = df[df["Lesson"] == lesson_choice]

    if not lesson_df.empty:
        st.sidebar.write(lesson_df)

        best = lesson_df["Score"].max()
        attempts = len(lesson_df)

        st.sidebar.metric("🔥 Best Score", best)
        st.sidebar.metric("📝 Attempts", attempts)
    else:
        st.sidebar.write("No scores yet")
else:
    st.sidebar.write("No scores yet")