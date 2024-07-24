from flask import Flask, render_template, request
app = Flask(__name__)
from backend.model import llm

from langchain_core.prompts import ChatPromptTemplate

user_state = {
    'stage': 'ask_role',
    'role': None,
    'jd': None,
    'resume': None,
    'history': []
}

def get_completion(prompt1, stage='', model="gpt-3.5-turbo"):
    system = "You are a helpful assistant that helps in preparing for interviews. You will be given the job role the user is applying for, the resume of the user, and the job description of the company the user is applying for. Ask questions one by one, take answers, and keep repeating for 10 questions."
    
    if stage == 'ask_resume':
        text = prompt1
    else:
        user_state['history'].append({'sender': 'human', 'text': prompt1})
        text = ''

    conversation_history = " ".join([f"{msg['sender']}: {msg['text']}" for msg in user_state['history']])
    human = f"{conversation_history} {text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | llm
    response = chain.invoke({"text": human})
    
    user_state['history'].append({'sender': 'assistant', 'text': response.content})
    
    return response.content

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get", methods=['GET'])
def get_bot_response():
    global user_state
    user_text = request.args.get('msg')
    # user_state['history'].append({'sender': 'user', 'text': user_text})
    # print(user_state)

    if user_state['stage'] == 'ask_role':
        user_state['role'] = user_text
        user_state['stage'] = 'ask_jd'
        response = "Please provide the job description for this role."
    elif user_state['stage'] == 'ask_jd':
        user_state['jd'] = user_text
        user_state['stage'] = 'ask_resume'
        response = "Please provide your resume now."
    elif user_state['stage'] == 'ask_resume':
        user_state['resume'] = user_text
        user_state['stage'] = 'ask_question'
        questions_prompt = (f"Generate interview questions based on the following job role: {user_state['role']}, "
                            f"job description: {user_state['jd']}, and resume: {user_state['resume']}.")
        response = get_completion(questions_prompt, stage  = 'ask_resume')
    else:
        response = get_completion(user_text, user_state['stage'])

    return response

if __name__ == "__main__":
    app.run(debug=True)
