import streamlit as st
import requests
import json
import boto3
import time

st.set_page_config(page_title="Question Generator", layout="wide")
API_URL = ""
client_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

s3 = boto3.client('s3')
bucket_name = 'question-generation-doping'
object_key = f'images/test1_q1.png'

s3_retrieved = s3.get_object(Bucket=bucket_name, Key=object_key)
content = s3_retrieved['Body'].read()

st.title("Geometry question")

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
        # Flow integration
        response = client_runtime.invoke_flow(
            flowIdentifier="arn:aws:bedrock:us-east-1:777179738691:flow/G11QQ4H770",
            flowAliasIdentifier="OTRTMJ0CDP",
            inputs=[
                {
                    "content": {
                        "document": user_input,
                    },
                    "nodeName": "FlowInputNode",
                    "nodeOutputName": "document",
                }
            ],
        )

        output_lines = []
        raw_events = []

        for event in response.get("responseStream"):
            raw_events.append(event)

            if "flowOutputEvent" in event:
                output_lines.append(event["flowOutputEvent"]["content"]["document"])
            elif "flowCompletionEvent" in event:
                output_lines.append(
                    f"Completed: {event['flowCompletionEvent']['completionReason']}"
                )


        result = output_lines[0]
        image_dict = output_lines[1]
        s3_uri = image_dict.get("s3_uri").split(bucket_name)[1][1:]
        print(s3_uri)

        object_key = s3_uri
        s3_retrieved = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = s3_retrieved['Body'].read()
        

        with st.chat_message("assistant"):
            st.image(content)
            st.write(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
else:
    with st.chat_message("assistant"):
        st.write("Size nasıl yardımcı olabilirim?")