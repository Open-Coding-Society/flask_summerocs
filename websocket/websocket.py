import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "websocket"}), 200


@app.get("/")
def index():
    return jsonify({"message": "websocket service running"}), 200


if __name__ == "__main__":
    # Keep this aligned with `websocket/docker-compose.yml`
    socketio.run(app, host="0.0.0.0", port=8590)