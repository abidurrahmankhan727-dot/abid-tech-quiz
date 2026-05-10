import streamlit as st
import requests
import random
import time

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻", layout="centered")

# ২. সিএসএস ডিজাইন (সুন্দর ইন্টারফেসের জন্য)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #28a745; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #218838; border: none; }
    .correct-box { background-color: #d4edda; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 6px solid #28a745; color: #155724; font-family: sans-serif; }
    .wrong-box { background-color: #f8d7da; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 6px solid #dc3545; color: #721c24; font-family: sans-serif; }
    .question-text { font-size: 20px; font-weight: 600; color: #1f1f1f; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ৩. প্রশ্ন নিয়ে আসার ফাংশন
def get_live_questions(count=10):
    try:
        url = f"https://opentdb.com/api.php?amount={count}&category=18&type=multiple"
        res = requests.get(url)
        data = res.json()
        if data['response_code'] == 0:
            return data['results']
    except Exception as e:
        return None
    return None

# ৪. সেশন স্টেট ইনিশিয়ালাইজেশন (Data Storage)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.user_answers = []
    st.session_state.current_options = None

# ৫. হেডার ও সাইডবার
st.title("🚀 ABID TECH QUIZ")
st.sidebar.header("⚙️ Quiz Dashboard")
num_questions = st.sidebar.slider("Select Questions", 5, 20, 10)

if st.sidebar.button("🔄 Start New Quiz"):
    with st.spinner("Loading fresh questions..."):
        questions = get_live_questions(num_questions)
        if questions:
            st.session_state.quiz_data = questions
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.user_answers = []
            st.session_state.current_options = None
            st.rerun()

# ৬. কুইজ চলাকালীন ইন্টারফেস
if st.session_state.quiz_data and not st.session_state.game_over:
    q_idx = st.session_state.current_q
    item = st.session_state.quiz_data[q_idx]
    
    # প্রশ্ন পরিষ্কার করা (HTML Entity Fix)
    clean_q = item['question'].replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    
    st.info(f"Question {q_idx + 1} of {len(st.session_state.quiz_data)}")
    st.markdown(f'<p class="question-text">{clean_q}</p>', unsafe_allow_html=True)
    
    # বর্তমান প্রশ্নের জন্য অপশন সেট করা (একবারই হবে)
    if st.session_state.current_options is None:
        opts = item['incorrect_answers'] + [item['correct_answer']]
        random.shuffle(opts)
        st.session_state.current_options = opts

    user_choice = st.radio("Choose the correct answer:", st.session_state
