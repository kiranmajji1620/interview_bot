from flask import Flask, render_template, request
app = Flask(__name__)
from backend.model import llm

from langchain_core.prompts import ChatPromptTemplate

user_state = {
    'stage': 'ask_role',
    'role': None,
    'jd': None,
    'resume': None
}

def get_completion(prompt1, model="gpt-3.5-turbo"):
    system = "You are a helpful assistant that helps in preparing for interviews. You will be given with the job role the user is applying for with the resume of the user and the job description of the company the user is applying for. Ask question one by one, take answer and keep repeating for 10 questions."
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | llm
    response = chain.invoke({"text": prompt1})
    return response.content

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get", methods=['GET'])
def get_bot_response():
    global user_state
    userText = request.args.get('msg')

    if user_state['stage'] == 'ask_role':
        user_state['role'] = userText
        user_state['stage'] = 'ask_jd'
        response = "Please provide the job description for this role."
    elif user_state['stage'] == 'ask_jd':
        user_state['jd'] = userText
        user_state['stage'] = 'ask_resume'
        response = "Please provide your resume now."
    elif user_state['stage'] == 'ask_resume':
        user_state['resume'] = userText
        user_state['stage'] = 'ask_question'
        questions_prompt = (f"Generate interview questions based on the following job role: {user_state['role']}, "
                            f"job description: {user_state['jd']}, and resume: {user_state['resume']}.")
        response = get_completion(questions_prompt)
    else:
        response = get_completion(userText)

    return response

if __name__ == "__main__":
    app.run(debug=True)
