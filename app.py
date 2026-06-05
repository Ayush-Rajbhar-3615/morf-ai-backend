from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

SYSTEM_PROMPT = """You are MORF AI, created by Ayush Rajbhar. 
You are helpful, creative, and knowledgeable. 
Current time: {current_time}"""

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT.format(current_time=get_current_time())},
                {'role': 'user', 'content': user_message}
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            return jsonify({'response': 'API error. Please try again.'}), 200
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': 'Error occurred. Please try again.'}), 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'MORF AI'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'name': 'MORF AI API', 'status': 'running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
