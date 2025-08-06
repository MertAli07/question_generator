import streamlit as st
import requests
import json
import boto3
import time

st.set_page_config(page_title="Question Generator", layout="wide")
API_URL = "https://csh7tdrm5k.execute-api.us-east-1.amazonaws.com/history_flow_invoke"
client_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

with st.sidebar:
    st.sidebar.title("Configuration")
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
        k_lecture = st.number_input("Lecture Count", min_value=1, max_value=10, value=1)
        k_question = st.number_input(
            "Question Count", min_value=1, max_value=10, value=1
        )

st.title("History Exam")

generate_test = 1 if multiple_questions else 0

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
        payload = {
            "question": user_input,
            "bloom": int(bloom_level),
            "multiple_question": generate_test,
            "k_lecture": int(k_lecture) if multiple_questions else 1,
            "k_question": int(k_question) if multiple_questions else 1,
        }
        response = requests.post(API_URL, json=payload)

        response_json = response.json()

        result = response_json["response"]

        with st.chat_message("assistant"):
            st.write(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
else:
    with st.chat_message("assistant"):
        st.write("Size nasıl yardımcı olabilirim?")
