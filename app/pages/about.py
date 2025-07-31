import streamlit as st

col1, col2 = st.columns(2, vertical_alignment="center")
with col1:
    st.image("app/assets/image.png", width=300)
with col2:
    st.title("Goaltech", anchor=False)
    st.write(
        "We are a team of passionate developers dedicated to creating innovative solutions that make learning more accessible and engaging. Our mission is to empower students and educators with cutting-edge technology."
    )

    st.link_button("Contact Us", "https://goaltech.com.tr/home", icon=":material/email:")
        