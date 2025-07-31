import streamlit as st
import requests
import json
import boto3
import time

st.set_page_config(page_title="Question Generator", layout="wide")
API_URL = ""
client_runtime = boto3.client("bedrock-agent-runtime")

with st.sidebar:
    st.sidebar.title("Configuration")
    lesson = st.selectbox(
        "Select a lesson",
        ("Math", "History"),
    )
    grade = st.selectbox(
        "Select a grade",
        ("9", "10", "11", "12"),
    )
    bloom_level = st.select_slider(
        "Select a Bloom's Taxonomy Level",
        options=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ],
    )

    multiple_questions = st.checkbox("Would you like to generate a test?")

    if multiple_questions:
        st.write("Great!")


st.title("Turkish Exam")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Generate Question")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Generating response..."):
        # FROM API
        question_json_str = json.dumps({"question": user_input})
        payload = {
            "question": question_json_str,
        }
        response = requests.post(API_URL, json=payload)
        # response.raise_for_status()

        response_json = response.json()

        answer = response_json["response"].split("Completed")[0]

        result = answer

        with st.chat_message("assistant"):
            st.write(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
            with st.expander("See more details"):
                st.write(response_json["raw_events"])
else:
    with st.chat_message("assistant"):
        st.write("Size nasıl yardımcı olabilirim?")
