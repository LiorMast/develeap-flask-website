from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<room>', methods=['GET'])
def join_room(room):
    return render_template('index.html', room=room)

@app.route('/api/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    log_file = os.path.join('logs', f'{room}.log')
    
    if request.method == 'POST':
        # Added .get() with a default to avoid crashing if 'msg' is missing
        user_message = request.form.get('msg', '')
        username = request.form.get('username', 'Anonymous')
        
        # Format: [2024-09-10 14:00:51] Roey: Hi everybody!
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] {username}: {user_message}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message)
            
        return jsonify({'response': 'Success'})
    else:
        # For GET requests (which updateChat does)
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()
        return "No messages yet\n"

if __name__ == '__main__':
    app.run(debug=True)