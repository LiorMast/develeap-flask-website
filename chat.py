from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

password = os.getenv('DB_PASSWORD')
hostname = os.getenv('DB_HOSTNAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@{hostname}:3306/chat_db'

db = SQLAlchemy(app)

if not os.path.exists('logs'):
    os.makedirs('logs')

@app.get("/")
def index():
    return render_template("index.html")

@app.route('/<room>', methods=['GET'])
def join_room(room):
    return render_template('index.html', room=room)

@app.post('/api/chat/<room>')
def chat(room):
    log_file = os.path.join('logs', f'{room}.log') # gets the room file
    
    if request.method == 'POST':
        user_message = request.form.get('msg', '').strip()
        username = request.form.get('username', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message content is required'}), 400    
        if not username:
            username = 'Anonymous'
        
        # Format: [2024-09-10 14:00:51] Roey: Hi everybody!
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"[{timestamp}] {username}: {user_message}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message)
            
        return jsonify({'response': 'Success'}), 201

@app.get("/api/chat/<room>")
def get_chat(room):
	room_file = os.path.join("./logs/", f"{room}.log")
	if not os.path.isfile(room_file):
		abort(404, description="Room not found")
	with open(room_file, "r", encoding="utf-8") as handle:
		return handle.read()
     
if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, host='0.0.0.0')
