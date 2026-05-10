import streamlit as st
import requests
import random
import time

# ওয়েবসাইটের নাম ও আইকন সেটআপ
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻", layout="centered")

# ডিজাইন সুন্দর করার জন্য কাস্টম সিএসএস (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    .stRadio>label { font-size: 18px; color: #333; }
    .correct-box { background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #28a745; }
    .wrong-box { background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #dc3545; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ABID TECH QUIZ")
st.write("Welcome! Practice ICT MCQs. Challenge your friends!")

# ইন্টারনেট থেকে প্রশ্ন নিয়ে আসার ফাংশন
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

# সেশন স্টেট (Quiz ডাটা এবং রেজাল্ট ধরে রাখার জন্য)
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.user_answers = [] # ইউজারের উত্তর জমা রাখার জন্য

# সাইডবার সেটিংস
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
            st.rerun()

# কুইজ ডিসপ্লে লজিক
if st.session_state.quiz_data and not st.session_state.game_over:
    q_idx = st.session_state.current_q
    item = st.session_state.quiz_data[q_idx]
    
    st.info(f"Question {q_idx + 1} of {len(st.session_state.quiz_data)}")
    
    # HTML কোড পরিষ্কার করা
    clean_q = item['question'].replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")
    st.subheader(clean_q)
    
    # অপশন শাফলিং
    if 'current_options' not in st.session_state or st.session_state.get('opt_idx') != q_idx:
        opts = item['incorrect_answers'] + [item['correct_answer']]
        random.shuffle(opts)
        st.session_state.current_options = opts
        st.session_state.opt_idx = q_idx

    user_choice = st.radio("Choose the correct option:", st.session_state.current_options, key=f"radio_{q_idx}")

    if st.button("Submit Answer"):
        # রেজাল্ট সেভ করা
        is_correct = user_choice == item['correct_answer']
        st.session_state.user_answers.append({
            "question": clean_q,
            "user_choice": user_choice,
            "correct_answer": item['correct_answer'],
            "is_correct": is_correct
        })
        
        if is_correct:
            st.success("🎯 Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {item['correct_answer']}")
        
        time.sleep(1)
        if q_idx + 1 < len(st.session_state.quiz_data):
            st.session_state.current_q += 1
        else:
            st.session_state.game_over = True
        st.rerun()

# কুইজ শেষ হওয়ার পর রিভিউ সেকশন
elif st.session_state.game_over:
    st.balloons()
    st.header("🏁 Quiz Result & Review")
    st.metric("Final Score", f"{st.session_state.score} / {len(st.session_state.quiz_data)}")
    
    st.subheader("📝 Review Your Answers:")
    
    for i, ans in enumerate(st.session_state.user_answers):
        if ans['is_correct']:
            st.markdown(f"""<div class="correct-box">
                <b>Q{i+1}: {ans['question']}</b><br>
                ✅ Your Answer: {ans['user_
