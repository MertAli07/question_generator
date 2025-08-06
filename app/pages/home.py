from pathlib import Path
import streamlit as st



st.title("🏫 Question Generator 🖌️")
st.write("This is the home page of the Question Generator app. Navigate to the sections to start generating questions.")

col1, col2 = st.columns(2, vertical_alignment="center")
with col1:
    st.header("Turkish Exams", divider=True)
    st.write("Generate questions for Turkish exams.")
    st.write("Explore various topics and levels and grades.")
    st.page_link(label="Start Generate Turkish Exams", page="pages/history_exam.py", icon=":material/book:")

with col2:
    st.header("English Exams", divider=True)
    st.write("Generate questions for English exams.")
    st.write("Explore various topics and levels and grades.")
    st.page_link(label="Start Generate English Exams", page="pages/english_exam.py", icon=":material/book_2:")

col3, col4 = st.columns(2, vertical_alignment="center")
with col3:
    st.header("Certification Exams", divider=True)
    st.write("Generate questions for certification exams.")
    st.write("Explore various topics and levels and grades.")
    st.page_link(label="Start Certification Exams", page="pages/certification_exam.py", icon=":material/license:")

with col4:
    st.header("Custom Exams", divider=True)
    st.write("Create your own custom exams.")
    st.write("Select topics, levels, and grades to generate tailored questions.")
    st.page_link(label="Start Custom Exams", page="pages/custom_exam.py", icon=":material/edit:")

st.write("Presented by _Goaltech_")
st.image("app/assets/image.png", width=300)

# home.py
authenticator = st.session_state.authenticator
st.sidebar.success(f"Welcome {st.session_state.name}!")
authenticator.logout("Logout", "sidebar")
