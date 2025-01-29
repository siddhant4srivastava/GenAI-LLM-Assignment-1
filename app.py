# app.py - Backend Implementation

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import openai
import os
import json
import markdown
import datetime

load_dotenv()

app = Flask(__name__)
app.config['KNOWLEDGE_PATH'] = 'knowledge_base/'
app.config['ADMIN_KEY'] = os.getenv('ADMIN_KEY')

# Initialize MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.faq_assistant

# Global knowledge store
knowledge_base = []

def load_knowledge():
    global knowledge_base
    knowledge_base = []
    
    for filename in os.listdir(app.config['KNOWLEDGE_PATH']):
        filepath = os.path.join(app.config['KNOWLEDGE_PATH'], filename)
        
        if filename.endswith('.json'):
            with open(filepath) as f:
                data = json.load(f)
                knowledge_base.extend(data['qa_pairs'])
                
        elif filename.endswith('.md'):
            with open(filepath) as f:
                content = markdown.markdown(f.read())
                knowledge_base.append({'content': content})
                
        elif filename.endswith('.txt'):
            with open(filepath) as f:
                knowledge_base.append({'content': f.read()})

def generate_response(question, context):
    prompt = f"""
    You are a helpful FAQ assistant. Answer the question based on the context below.
    If you can't answer, say "I don't know. Please contact support."

    Context: {context}
    Question: {question}
    Answer:"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return "I'm having trouble answering right now. Please try again later."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data['question']
    
    # Simple context retrieval (can be enhanced with vector search)

    context = "\n".join([item.get('content', '') for item in knowledge_base[:3]])
    
    answer = generate_response(question, context)
    
    # Log interaction
    db.interactions.insert_one({
        'question': question,
        'answer': answer,
        'timestamp': datetime.datetime.utcnow()
    })
    
    return jsonify({'answer': answer})

@app.route('/admin/update', methods=['POST'])
def update_knowledge():
    if request.headers.get('X-Admin-Key') != app.config['ADMIN_KEY']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    load_knowledge()
    return jsonify({'message': f'Knowledge base updated with {len(knowledge_base)} items'})

@app.route('/admin/logs', methods=['GET'])
def get_logs():
    if request.headers.get('X-Admin-Key') != app.config['ADMIN_KEY']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    logs = list(db.interactions.find().sort('timestamp', -1).limit(100))
    for log in logs:
        log['_id'] = str(log['_id'])
        
    return jsonify(logs)

if __name__ == '__main__':
    load_knowledge()
    app.run(debug=True)