from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import ChatOllama
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
import pandas as pd
import re
from tqdm import tqdm

load_dotenv()

system_prompt = """
You are a helpful and accurate math-solving assistant. Your task is to determine whether a given math question is solvable and, if it is, provide the correct solution.
Instructions:
1. If the question is clearly solvable (e.g., a well-formed math problem with a valid solution), set is_solvable to true, leave denial as an empty string, and provide the correct solution as a string in answer. Ensure the answer is concise but complete.
2. If the question is not solvable (e.g., it's ambiguous, incomplete, contradictory, or not a math problem), set is_solvable to false, provide a clear and polite explanation in denial, and leave answer as an empty string.
3. Never fabricate solutions to unsolvable problems. Be honest and precise.
"""


class AgentResponse(BaseModel):
    """Respond to the user in this format."""

    isSolvable: bool = Field(
        alias="is_solvable", description="Is the question solvable?"
    )
    denial: str = Field(
        alias="denial", description="If the question is not solvable, explain why."
    )
    answer: str = Field(
        alias="answer", description="If the question is solvable, provide the answer."
    )
    correctChoice: str = Field(
        alias="correct_choice",
        description="If the question is a multiple-choice question, provide the correct choice.",
    )

    class Config:
        allow_population_by_alias = True


tools = load_tools(["wolfram-alpha"])
# llm = ChatOllama(model="gemma3:1b")

llm = ChatBedrockConverse(
    model_id=os.getenv("SELECTED_MODEL_ARN"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
    provider="amazon",
)

agent = create_react_agent(
    model=llm,
    tools=tools,
    response_format=AgentResponse,
    prompt=system_prompt,
)

labels = ["A", "B", "C", "D", "E"]

df = pd.read_csv("dataset/Mat_sorular.csv")


def extract_and_format(choice_str):
    # Extract values between quotes or standalone words/numbers
    values = re.findall(r"'(.*?)'", choice_str)
    # Format only as many labels as available
    return " ".join(f"{label}){val}" for label, val in zip(labels, values))

df["formatted_choices"] = df["choices"].apply(extract_and_format)

model_answer = []
correct_anwers = 0
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    question = row["question"]
    formatted_choices = row["formatted_choices"]
    correct_choice = row["answer"]
    input_data = question + "\n" + formatted_choices
    inputs = {
        "messages": [
            (
                "user",
                input_data,
            )
        ]
    }
    response = agent.invoke(inputs)
    result: AgentResponse = response["structured_response"]
    model_answer.append(result.correctChoice)
    if result.correctChoice == correct_choice:
        correct_anwers += 1
    print(f"Correct: {correct_anwers}")
    print(f"Total: {index + 1}")
    print(f"Accuracy: {correct_anwers / (index + 1)}")


# inputs = {
#     "messages": [
#         (
#             "user",
#             """
#                 Bir kargo şirketi, şehirdeki teslimat rotalarını optimize etmek istiyor. Şehir, kuzey-güney ve doğu-batı yönlerinde uzanan sokaklar ile karelerden oluşan bir ızgara şeklindedir. Depo A noktasında (0,0) konumundadır. Kargo şirketi, B müşterisine (3,4) konumunda teslimat yaptıktan sonra C müşterisine (6,2) konumunda teslimat yapacaktır. Şirket, toplam yakıt tüketimini minimize etmek için her iki teslimatı da en kısa yoldan yapmak istiyor. A'dan B'ye, sonra B'den C'ye giderken kullanılabilecek toplam farklı rota kombinasyonu sayısını veren bir formül tasarlayınız ve bu formülü kullanarak sonucu hesaplayınız.
#             """,
#         )
#     ]
# }
# response = agent.invoke(inputs)
# result: AgentResponse = response["structured_response"]
# print(result.isSolvable)
# print(result.answer)
# print(result.denial)
