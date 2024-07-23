from dotenv import load_dotenv
import os
load_dotenv()  
groq_api_key = os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq
llm = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key = groq_api_key
)