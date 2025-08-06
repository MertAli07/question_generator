import streamlit as st
import requests
import json
import pyperclip


def copy_to_clipboard(data: dict):
    """Function to copy text to clipboard."""
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    pyperclip.copy(json_str)


API_URL = "https://a1a58ot3ih.execute-api.us-east-1.amazonaws.com/invoke"

st.set_page_config(layout="wide")
st.title("Generate Math Questions")
st.write(
    "This page allows you to generate questions specifically for Turkish exams. Choose the type of question you want to create."
)

st.header("Question Topics")

# Sample hierarchical data
content_tree = {
    "Sayma ve Olasılık": {
        "Sıralama ve Seçme": {
            "Sayma Yöntemleri": [
                "BİRE BİR EŞLEME YOLUYLA SAYMA",
                "TOPLAMA YOLUYLA SAYMA",
                "ÇARPMA YOLUYLA SAYMA",
            ],
            "Faktöriyel": [
                "FAKTÖRİYEL NEDİR",
                "FAKTÖRİYEL İLE SAYMANIN TEMEL PRENSİBİ İLİŞKİSİ",
            ],
            "Permütasyon": ["PERMÜTASYON SAYISI", "TEKRARLI PERMÜTASYON"],
            "All": ["All"],
        },
        "Basit Olayların Olasılıkları": {
            "Kombinasyon": ["KOMBİNASYON", "KOMBİNASYON SAYISI"],
            "Pascal Üçgeni ve Binom Açılımı": [
                "PASCAL ÜÇGENİ – BİNOM AÇILIMI İLİŞKİSİ",
                "BİNOM AÇILIMININ ÖZELLİKLERİ",
            ],
            "Olasılık": ["OLASILIK KAVRAMLARI", "OLASILIK HESAPLAMA"],
            "All": ["All"],
        },
        "All": {"All": ["All"]},
    }
}

col1, col2 = st.columns(2)

with col1:
    # First select: unit
    unit = st.selectbox("Select Unit", list(content_tree.keys()))

    # Second select: sub_unit
    sub_units = list(content_tree[unit].keys())
    sub_unit = st.selectbox("Select Sub-Unit", sub_units)

with col2:
    # Third select: topic
    topics = list(content_tree[unit][sub_unit].keys())
    topic = st.selectbox("Select Topic", topics)

    # Fourth select: headline
    headlines = content_tree[unit][sub_unit][topic]
    headline = st.selectbox("Select Title", headlines)

payload = {
    "unit": unit,
    "subject": sub_unit,
    "sub_subject": topic,
    "title": headline,
}

col3, col4 = st.columns(2)

with col3:
    selected_title, copy_icon = st.columns(2)
    with selected_title:
        st.header("You Selected", anchor=False)
    with copy_icon:
        st.button(
            "Copy to Clipboard",
            key="copy_button",
            use_container_width=True,
            on_click=copy_to_clipboard(payload),
            icon=":material/content_copy:",
        )
    st.markdown(
        f"**Unit:** {unit}\n- **Sub-unit:** {sub_unit}\n- **Topic:** {topic}\n- **Headline:** {headline}"
    )

response_data = None
with col4:
    # Button to generate question
    if st.button("Generate Question", use_container_width=True):
        with st.spinner("Generating question..."):

            response = requests.post(API_URL, json=payload)
            response_data = response.json()

if response_data:
    st.header("Generated Question:")
    print(response_data)
    st.write(response_data["response"])
