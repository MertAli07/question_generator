from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from dotenv import load_dotenv
import os
import pandas as pd
import ast
import re

load_dotenv()

labels = ['A', 'B', 'C', 'D', 'E']

df = pd.read_csv("dataset/Mat_sorular.csv")

def extract_and_format(choice_str):
    # Extract values between quotes or standalone words/numbers
    values = re.findall(r"'(.*?)'", choice_str)
    # Format only as many labels as available
    return ' '.join(f"{label}){val}" for label, val in zip(labels, values))

# Apply the function
df['formatted_choices'] = df['choices'].apply(extract_and_format)


print(df[['choices', 'formatted_choices']])
