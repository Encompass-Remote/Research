import os
from openai import OpenAI
from dotenv import load_dotenv
import langchain
from langchain_community.llms import OpenAI

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_KEY")

if api_key is None:
    raise ValueError("OPENAI_KEY not found in environment variables. Please check your .env file.")

llm = OpenAI(temperature=0.9, openai_api_key=api_key)

response = llm.predict("Suggest me a skill that is in demand?")
print(response)