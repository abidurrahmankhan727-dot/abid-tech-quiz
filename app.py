import streamlit as st
import requests
import random
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻", layout="centered")

# ২. ডিজাইন সুন্দর করার জন্য কাস্টম সিএসএস (CSS)
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

# ৩. ইন্টারনেট থেকে প্রশ্ন নিয়ে আসার ফাংশন
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

# ৪. সেশন স্টেট (Quiz ডাটা এবং রিভিউ জমা রাখার জন্য)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.user_answers = [] # ইউজারের সব উত্তর এখানে জমা থাকবে
    st.session_state.current_options = []

# ৫. সাইডবার সেটিংস
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
            st.session_state.user_answers = []
            st.session_state.current_options = []
            st.rerun()

# ৬. কুইজ ডিসপ্লে লজিক
if st.session_state.quiz_data and not st.session_state.game_over:
    q_idx = st.session_state.current_q
    item = st.session_state.quiz_data[q_idx]
    
    st.info(f"Question {q_idx + 1} of {len(st.session_state.quiz_data)}")
    
    # HTML কোড পরিষ্কার করা
    clean_q = item['question'].replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")
    st.subheader(clean_q)
