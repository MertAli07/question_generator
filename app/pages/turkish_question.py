import streamlit as st

st.title("Generate Turkish Questions")
st.write("This page allows you to generate questions specifically for Turkish exams. Choose the type of question you want to create.")

st.header("Question Topics")

# Sample hierarchical data
content_tree = {
    "Sayma ve Olasılık": {
        "Sıralama ve Seçme": {
            "Sayma Yöntemleri": ["BİRE BİR EŞLEME YOLUYLA SAYMA", "TOPLAMA YOLUYLA SAYMA", "ÇARPMA YOLUYLA SAYMA"],
            "Faktöriyel": ["FAKTÖRİYEL NEDİR?", "FAKTÖRİYEL İLE SAYMANIN TEMEL PRENSİBİ İLİŞKİSİ"],
            "Permütasyon": ["PERMÜTASYON SAYISI", "TEKRARLI PERMÜTASYON"],
            "All": ["All"]
        },
        "Basit Olayların Olasılığı": {
            "Kombinasyon": ["KOMBİNASYON", "KOMBİNASYON SAYISI"],
            "Paskal Üçgeni ve Binom Açılımı": ["PASCAL ÜÇGENİ – BİNOM AÇILIMI İLİŞKİSİ", "BİNOM AÇILIMININ ÖZELLİKLERİ"],
            "Olasılık": ["OLASILIK KAVRAMLARI", "OLASILIK HESAPLAMA"],
            "All": ["All"]
        },
        "All": {
            "All": ["All"]
        }
    }
}

# First select: unit
unit = st.selectbox("Select Unit", list(content_tree.keys()))

# Second select: sub_unit
sub_units = list(content_tree[unit].keys())
sub_unit = st.selectbox("Select Sub-Unit", sub_units)

# Third select: topic
topics = list(content_tree[unit][sub_unit].keys())
topic = st.selectbox("Select Topic", topics)

# Fourth select: headline
headlines = content_tree[unit][sub_unit][topic]
headline = st.selectbox("Select Headline", headlines)

# Display selection
st.markdown(f"### You selected:\n- **Unit:** {unit}\n- **Sub-unit:** {sub_unit}\n- **Topic:** {topic}\n- **Headline:** {headline}")