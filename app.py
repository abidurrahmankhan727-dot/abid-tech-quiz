import streamlit as st
import requests
import random
import time

# Page config
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ABID TECH QUIZ")

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

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False

st.sidebar.header("⚙️ Quiz Settings")
num_questions = st.sidebar.slider("Select Questions", 5, 25, 10)

if st.sidebar.button("🔄 Start New Quiz"):
    questions = get_live_questions(num_questions)
    if questions:
        st.session_state.quiz_data = questions
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.rerun()

if st.session_state.quiz_data and not st.session_state.game_over:
    q_idx = st.session_state.current_q
    item = st.session_state.quiz_data[q_idx]
    
    st.info(f"Question {q_idx + 1} of {len(st.session_state.quiz_data)}")
    clean_q = item['question'].replace("&quot;", '"').replace("&#039;", "'")
    st.subheader(clean_q)
    
    if 'current_options' not in st.session_state or st.session_state.get('last_q') != q_idx:
        opts = item['incorrect_answers'] + [item['correct_answer']]
        random.shuffle(opts)
        st.session_state.current_options = opts
        st.session_state.last_q = q_idx

    user_choice = st.radio("Choose:", st.session_state.current_options, key=f"q_{q_idx}")

    if st.button("Submit"):
        if user_choice == item['correct_answer']:
            st.success("🎯 Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct: {item['correct_answer']}")
        
        time.sleep(1)
        if q_idx + 1 < len(st.session_state.quiz_data):
            st.session_state.current_q += 1
        else:
            st.session_state.game_over = True
        st.rerun()

elif st.session_state.game_over:
    st.balloons()
    st.header("🏁 Quiz Result")
    st.metric("Score", f"{st.session_state.score} / {len(st.session_state.quiz_data)}")
    if st.button("Restart"):
        st.session_state.quiz_data = []
        st.session_state.game_over = False
        st.rerun()
else:
    st.warning("👈 Sidebar-এর 'Start New Quiz' বাটনে ক্লিক করুন!")
