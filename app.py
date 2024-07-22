from flask import Flask, render_template, request
app = Flask(__name__)

from dotenv import load_dotenv
import os
load_dotenv()  
groq_api_key = os.getenv("GROQ_API_KEY")

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
chat = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key = groq_api_key
)

def get_completion(prompt1, model="gpt-3.5-turbo"):
    system = "You are a helpful assistant."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    response = chain.invoke({"text": prompt1})
    # print(prompt)
    # print(response.content)
    return response.content

@app.route("/")
def home():    
    return render_template("index.html")
@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')  
    response = get_completion(userText)  
    #return str(bot.get_response(userText)) 
    return response
if __name__ == "__main__":
    app.run(debug=True)