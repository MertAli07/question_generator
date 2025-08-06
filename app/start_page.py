from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth
import pickle

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
    "usernames": {
        "mert": {
            "name": "Mert Ali Yalçın",
            "password": hashed_passwords[0],
        },
        "gorkem": {
            "name": "Görkem Yağmur",
            "password": hashed_passwords[1],
        },
        "ugur": {
            "name": "Uğur Yiğit",
            "password": hashed_passwords[2],
        },
    }
}

if "authenticator" not in st.session_state:
    st.session_state.authenticator = stauth.Authenticate(
        credentials,
        "question_generator",
        "abcdef",
        cookie_expiry_days=30
    )

authenticator = st.session_state.authenticator

name, authentication_status, username = authenticator.login(
    location="main",
    key="login"
)

st.session_state.name = name

if authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
else:
    

    history_exam_page = st.Page(
        page="pages/history_exam.py",
        title="History Exam",
        icon=":material/book:",
    )

    english_exam_page = st.Page(
        page="pages/english_exam.py",
        title="English Exam",
        icon=":material/book_2:",
    )

    about_page = st.Page(
        page="pages/about.py",
        title="About Us",
        icon=":material/info:",
    )

    home_page = st.Page(
        page="pages/home.py",
        title="Home",
        icon=":material/home:",
    )

    certification_exam_page = st.Page(
        page="pages/certification_exam.py",
        title="Certification Exam",
        icon=":material/license:",
    )

    custom_exam_page = st.Page(
        page="pages/custom_exam.py",
        title="Custom Exam",
        icon=":material/edit:",
    )

    math_question_page= st.Page(
        page="pages/math_question.py",
        title="Math Question",
        icon=":material/question_answer:",
    )

    pg = st.navigation(
        {
            "Home": [home_page],
            "Exams": [math_question_page, history_exam_page, english_exam_page, certification_exam_page, custom_exam_page],
            "About Us": [about_page],
        }
    )

    st.logo("app/assets/image_2.png", size="large")

    pg.run()
