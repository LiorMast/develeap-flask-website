from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

password = os.getenv('DB_PASSWORD')
hostname = os.getenv('DB_HOSTNAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@{hostname}:3306/chat_db'

db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = 'messages'

    # Mapping the columns
    timestamp = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    room = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f'[{self.timestamp}] {self.username}: {self.message}\n'

@app.get("/")
def index():
    return render_template("index.html")

@app.route('/<room>', methods=['GET'])
def join_room(room):
    return render_template('index.html', room=room)

@app.post('/api/chat/<room>')
def chat(room):
    if request.method == 'POST':
        user_message = request.form.get('msg', '').strip()
        username = request.form.get('username', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message content is required'}), 400    
        if not username:
            username = 'Anonymous'
        
        # Format: [2024-09-10 14:00:51] Roey: Hi everybody!
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        new_message = Message(timestamp=timestamp, room=room, username=username, message=user_message)
        db.session.add(new_message)
        db.session.commit()
            
        return jsonify({'response': 'Success'}), 201

@app.get("/api/chat/<room>")
def get_chat(room):
    msgs = Message.query.filter_by(room=room).all()
    return "".join(repr(msg) for msg in msgs)
     
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
