import os

from flask import Flask, abort, send_file

app = Flask(__name__)


@app.get("/")
def index():
	return send_file("index.html")


@app.get("/api/chat/<room>")
def get_chat(room):
	room_file = os.path.join("./chat_rooms_mock/", f"{room}")
	if not os.path.isfile(room_file):
		abort(404, description="Room not found")
	with open(room_file, "r", encoding="utf-8") as handle:
		return handle.read()

