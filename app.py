 import streamlit as st
import requests
import random
import time
# ওয়েবসাইটের নাম ও আইকন সেটআপ
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻", layout="centered")

# ডিজাইন সুন্দর করার জন্য কাস্টম সিএসএস (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    .stRadio>label { font-size: 18px; color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ABID TECH QUIZ")
st.write("Welcome! Practice ICT MCQs directly from the internet. Challenge your friends!")

# ইন্টারনেট থেকে প্রশ্ন নিয়ে আসার ফাংশন
def get_live_questions(count=10):
    try:
        # Category 18 = Computer Science
        url = f"https://opentdb.com/api.php?amount={count}&category=18&type=multiple"
        res = requests.get(url)
        data = res.json()
        if data['response_code'] == 0:
            return data['results']
    except:
        return None
    return None

# সেশন স্টেট (Quiz ডাটা ধরে রাখার জন্য)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False

# সাইডবার সেটিংস
st.sidebar.header("⚙️ Quiz Settings")
num_questions = st.sidebar.slider("Select Number of Questions", 5, 25, 10)

if st.sidebar.button("🔄 Start New Quiz / Fetch Questions"):
    with st.spinner("Fetching fresh questions from internet..."):
        questions = get_live_questions(num_questions)
        if questions:
            st.session_state.quiz_data = questions
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.rerun()
        else:
            st.error("Failed to fetch questions. Please check internet connection.")

# কুইজ ডিসপ্লে লজিক
if st.session_state.quiz_data and not st.session_state.game_over:
    q_idx = st.session_state.current_q
    item = st.session_state.quiz_data[q_idx]
    
    st.info(f"Question {q_idx + 1} of {len(st.session_state.quiz_data)}")
    
    # HTML কোড পরিষ্কার করে প্রশ্ন দেখানো (যেমন &quot; এর বদলে " দেখানো)
    clean_q = item['question'].replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")
    st.subheader(clean_q)
    
    # অপশনগুলো সাজানো (শাফলিং)
    if 'current_options' not in st.session_state or st.session_state.opt_idx != q_idx:
        opts = item['incorrect_answers'] + [item['correct_answer']]
        random.shuffle(opts)
        st.session_state.current_options = opts
        st.session_state.opt_idx = q_idx

    user_choice = st.radio("Choose the correct option:", st.session_state.current_options, key=f"radio_{q_idx}")

    if st.button("Submit Answer"):
        if user_choice == item['correct_answer']:
            st.success("🎯 Correct! Well done.")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! The correct answer was: {item['correct_answer']}")
        
        time.sleep(1.5)
        if q_idx + 1 < len(st.session_state.quiz_data):
            st.session_state.current_q += 1
        else:
            st.session_state.game_over = True
        st.rerun()

elif st.session_state.game_over:
    st.balloons()
    st.header("🏁 Quiz Result")
    st.metric("Final Score", f"{st.session_state.score} / {len(st.session_state.quiz_data)}")
    if st.button("Play Again"):
        st.session_state.quiz_data = []
        st.session_state.game_over = False
        st.rerun()
else:
    st.warning("👈 Use the sidebar to click 'Start New Quiz' and get questions!")                                                                                                                                                           
                                                                                                                                                              
                                                                                                                                 
