import streamlit as st
import requests
import random

# টাইটেল
st.title("🚀 ABID TECH QUIZ")

# কুইজ ডেটা লোড করা
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
    st.session_state.score = 0

# একটি সিম্পল বাটন
if st.button("Start Quiz"):
    st.write("কুইজ শুরু হচ্ছে...")
    st.success("আপনার কোড এখন ঠিকভাবে কাজ করছে!")
