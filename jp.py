import streamlit as st
import random
import os
import csv
import pandas as pd

st.set_page_config(page_title="JLPT Practice App", layout="centered")

st.title("🇯🇵 JLPT Practice App")

# 📚 Lessons data
lessons = {
    "Lesson 1 Vocabulary": [
        {"question": "I (polite)", "jp": "わたし", "en": "watashi"},
        {"question": "You", "jp": "あなた", "en": "anata"},
        {"question": "That person (normal)", "jp": "あのひと", "en": "ano hito"},
        {"question": "That person (polite)", "jp": "あのかた", "en": "ano kata"},
        {"question": "Mr/Ms", "jp": "さん", "en": "san"},
        {"question": "Child suffix", "jp": "ちゃん", "en": "chan"},
        {"question": "Boy suffix", "jp": "くん", "en": "kun"},
        {"question": "Nationality suffix", "jp": "じん", "en": "jin"},
        {"question": "Teacher", "jp": "せんせい", "en": "sensei"},
        {"question": "Student", "jp": "がくせい", "en": "gakusei"},
        {"question": "Company employee", "jp": "かいしゃいん", "en": "kaishain"},
        {"question": "Bank employee", "jp": "ぎんこういん", "en": "ginkouin"},
        {"question": "Doctor", "jp": "いしゃ", "en": "isha"},
        {"question": "Who (normal)", "jp": "だれ", "en": "dare"},
        {"question": "Who (polite)", "jp": "どなた", "en": "donata"},
        {"question": "How old (normal)", "jp": "なんさい", "en": "nansai"},
        {"question": "How old (polite)", "jp": "おいくつ", "en": "oikutsu"},
        {"question": "Nice to meet you", "jp": "はじめまして", "en": "hajimemashite"},
    ],

    "Lesson 1 Grammar": [
        {"question": "Topic marker", "jp": "は", "en": "wa"},
        {"question": "Is/am/are", "jp": "です", "en": "desu"},
        {"question": "Not (polite)", "jp": "じゃありません", "en": "ja arimasen"},
        {"question": "Question marker", "jp": "か", "en": "ka"},
        {"question": "Of / belonging", "jp": "の", "en": "no"},
    ],

    "Lesson 1 Sentences": [
        {"question": "I am a student", "jp": "わたしはがくせいです", "en": "watashi wa gakusei desu"},
        {"question": "I am not a teacher", "jp": "わたしはせんせいじゃありません", "en": "watashi wa sensei ja arimasen"},
        {"question": "Who is that person?", "jp": "あのひとはだれですか", "en": "ano hito wa dare desu ka"},
        {"question": "I am Indian", "jp": "わたしはインドじんです", "en": "watashi wa indo jin desu"},
        {"question": "Nice to meet you", "jp": "はじめまして", "en": "hajimemashite"},
        {"question": "Yes, that's right", "jp": "はいそうです", "en": "hai sou desu"},
        {"question": "No, I am not", "jp": "いいえちがいます", "en": "iie chigaimasu"},
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
