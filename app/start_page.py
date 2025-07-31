import streamlit as st

turkish_exam_page = st.Page(
    page="pages/turkish_exam.py",
    title="Turkish Exam",
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



pg = st.navigation(
    {
        "Home": [home_page],
        "Exams": [turkish_exam_page, english_exam_page, certification_exam_page, custom_exam_page],
        "About Us": [about_page],
    }
)

st.logo("app/assets/image_2.png", size="large")

pg.run()
