from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from dotenv import load_dotenv
import os
import pandas as pd
import ast
import re
import boto3

client_kb = boto3.client("bedrock-agent", region_name="us-east-1")
response = client_kb.list_knowledge_bases()
print(response)

