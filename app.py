import streamlit as st
import time
import random

# ওয়েবসাইটের কনফিগারেশন
st.set_page_config(page_title="ABID TECH QUIZ", page_icon="💻")

# কুইজ ডাটাবেস (নমুনা হিসেবে ১০টি দেওয়া হলো, আপনি আরও যোগ করতে পারেন)
questions_db = [
    {"q": "What is the full form of DNS?", "a": "Domain Name System", "options": ["Domain Name System", "Data Name System", "Digital Network Service", "Direct Node Serial"]},
    {"q": "Which is the 'Brain' of the computer?", "a": "CPU", "options": ["RAM", "CPU", "Hard Disk", "Monitor"]},
    {"q": "What does HTML stand for?", "a": "Hypertext Markup Language", "options": ["Hyperlink Text Markup Language", "Hypertext Markup Language", "Home Tool Markup Language", "Hypertext Machine Language"]},
    {"q": "Which of the following is a search engine?", "a": "Google", "options": ["Facebook", "Google", "WhatsApp", "Windows"]},
    {"q": "1 Gigabyte (GB) = ?", "a": "1024 MB", "options": ["1000 MB", "1024 MB", "512 MB", "1024 KB"]},
    {"q": "What is the shortcut key for Copy?", "a": "Ctrl + C", "options": ["Ctrl + V", "Ctrl + X", "Ctrl + C", "Ctrl + Z"]},
    {"q": "Which is a volatile memory?", "a": "RAM", "options": ["ROM", "RAM", "Hard Disk", "SSD"]},
    {"q": "What is the full form of URL?", "a": "Uniform Resource Locator", "options": ["Uniform Resource Locator", "Universal Radio Link", "United Resource Line", "Unique Resource Locator"]},
    {"q": "Who is the developer of Python?", "a": "Guido van Rossum", "options": ["Mark Zuckerberg", "Bill Gates", "Guido van Rossum", "Steve Jobs"]},
    {"q": "Which protocol is used to send emails?", "a": "SMTP", "options": ["HTTP", "FTP", "SMTP", "IP"]}
]

# হেডার সেকশন
st.title("🚀 ABID TECH QUIZ")
st.subheader("Test your ICT knowledge with your friends!")

# কাস্টমাইজেশন অপশন
num_q = st.sidebar.slider("Select Number of Questions", 5, len(questions_db), 10)
time_limit = st.sidebar.number_input("Time limit per question (seconds)", 10, 60, 20)

if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.score = 0
    st.session_state.current_index = 0

def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.score = 0
    st.session_state.current_index = 0
    random.shuffle(questions_db)
    st.session_state.selected_questions = questions_db[:num_q]

if not st.session_state.quiz_started:
    if st.button("Start Quiz"):
        start_quiz()
        st.rerun()
else:
    q_list = st.session_state.selected_questions
    idx = st.session_state.current_index
    
    if idx < len(q_list):
        st.write(f"### Question {idx + 1} of {len(q_list)}")
        current_q = q_list[idx]
        
        # টাইমার বার
        placeholder = st.empty()
        for t in range(time_limit, -1, -1):
            placeholder.metric("⏳ Time Remaining", f"{t}s")
            time.sleep(1)
            if t == 0:
                st.warning("Time's up!")
                st.session_state.current_index += 1
                st.rerun()
            
            # অপশন সিলেকশন (এটি টাইমারের মাঝখানে ইউজার ক্লিক করলে ব্রেক করবে না)
            answer = st.radio("Choose the correct answer:", current_q["options"], key=f"q_{idx}")
            
            if st.button("Submit Answer", key=f"btn_{idx}"):
                if answer == current_q["a"]:
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error(f"Wrong! Correct answer was: {current_q['a']}")
                
                time.sleep(1)
                st.session_state.current_index += 1
                st.rerun()
                break
    else:
        st.balloons()
        st.write("## 🎉 Quiz Completed!")
        st.write(f"### Your Final Score: {st.session_state.score} out of {len(q_list)}")
        if st.button("Play Again"):
            st.session_state.quiz_started = False
            st.rerun()
