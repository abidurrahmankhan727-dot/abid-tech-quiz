import streamlit as st
import requests
import random
import time

# পেজ সেটআপ
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻", layout="centered")

# ডিজাইন সুন্দর করার জন্য কাস্টম সিএসএস (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    .stRadio>label { font-size: 18px; color: #333; }
    .correct-box { background-color: #d4edda; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #28a745; color: #155724; }
    .wrong-box { background-color: #f8d7da; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #dc3545; color: #721c24; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ABID TECH QUIZ")
st.write("Welcome! Practice ICT MCQs. Challenge your friends!")

# ইন্টারনেট থেকে প্রশ্ন নিয়ে আসার ফাংশন
def get_live_questions(count=10):
    try:
        url = f"https://opentdb.com/api.php?amount={count}&category=18&type=multiple"
        res = requests.get(url)
        data = res.json()
        if data['response_code'] == 0:
            return data['results']
    except:
        return None
    return None

# সেশন স্টেট সেটআপ
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.user_answers = []
    st.session_state.current_options = []

# সাইডবার
st.sidebar.header("⚙️ Quiz Settings")
num_questions = st.sidebar.slider("Select Number of Questions", 5, 25, 10)

if st.sidebar.button("🔄 Start New Quiz"):
    with st.spinner("Fetching questions..."):
        questions = get_live_questions(num_questions)
        if questions:
            st.session_state.quiz_data = questions
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session
