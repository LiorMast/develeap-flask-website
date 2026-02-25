from flask import Flask, render_template, request, jsonify, abort
from datetime import datetime
import os
import pymysql

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'chatuser'),
    'password': os.environ.get('DB_PASSWORD', 'chatpass'),
    'database': os.environ.get('DB_NAME', 'chatdb'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """Establish a database connection"""
    return pymysql.connect(**DB_CONFIG)

@app.get("/")
def index():
    return render_template("index.html")

@app.route('/<room>', methods=['GET'])
def join_room(room):
    return render_template('index.html', room=room)

@app.post('/api/chat/<room>')
def chat(room):
    user_message = request.form.get('msg', '').strip()
    username = request.form.get('username', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message content is required'}), 400    
    if not username:
        username = 'Anonymous'
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO messages (username, room, msg) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, room, user_message))
        connection.commit()
        connection.close()
        
        return jsonify({'response': 'Success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.get("/api/chat/<room>")
def get_chat(room):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT username, timestamp, msg FROM messages WHERE room = %s ORDER BY timestamp ASC"
            cursor.execute(sql, (room,))
            messages = cursor.fetchall()
        connection.close()
        
        if not messages:
            return jsonify({'messages': [], 'info': 'No messages in this room yet'}), 200
        
        # Format messages like the original file format: [timestamp] username: message
        formatted_messages = []
        for msg in messages:
            timestamp = msg['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            formatted_messages.append(f"[{timestamp}] {msg['username']}: {msg['msg']}")
        
        return '\n'.join(formatted_messages) + '\n'
    except Exception as e:
        return jsonify({'error': str(e)}), 500
     
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)






