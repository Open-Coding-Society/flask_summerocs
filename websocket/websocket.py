import gevent
from gevent import pywsgi

from flask import Flask, jsonify, request
from flask_socketio import SocketIO

import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

@app.get("/health")
def health():
    # Get current server time
    server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    # Try to get client IP
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    # Latency: if client sends ?ping=timestamp, return round-trip
    ping = request.args.get("ping")
    latency = None
    if ping:
        try:
            latency = time.time() - float(ping)
        except Exception:
            latency = None
    resp = {
        "ok": True,
        "service": "websocket",
        "server_time_utc": server_time,
        "client_ip": client_ip,
        "latency_seconds": latency,
        "info": "Send ?ping=<epoch_seconds> to measure latency."
    }
    return jsonify(resp), 200

players = {}


@app.get("/")
def index():
    return jsonify({"message": "websocket service running"}), 200

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    # Spawn at random or default position
    players[sid] = {"x": 100, "y": 100}
    print(f"[SERVER] Player joined: {sid}")
    socketio.emit('player_update', {"players": players})
    
@socketio.on('move')
def handle_move(data):
    sid = request.sid
    if sid in players and "x" in data and "y" in data:
        players[sid]["x"] = data["x"]
        players[sid]["y"] = data["y"]
        socketio.emit('player_update', {"players": players})

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in players:
        del players[sid]
        socketio.emit('player_left', {"sid": sid})
        socketio.emit('player_update', {"players": players})

# Socket.IO event for live status (same info as /health)
@socketio.on('get_live_status')
def handle_live_status(data=None):
    server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ping = None
    latency = None
    # If client sends {"ping": <epoch_seconds>} as payload, calculate latency
    if data and isinstance(data, dict):
        ping = data.get("ping")
    if ping:
        try:
            latency = time.time() - float(ping)
        except Exception:
            latency = None
    resp = {
        "ok": True,
        "service": "websocket",
        "server_time_utc": server_time,
        "client_ip": client_ip,
        "latency_seconds": latency,
        "info": "Send {ping: <epoch_seconds>} as payload to measure latency."
    }
    socketio.emit('live_status', resp, room=request.sid)
    
if __name__ == "__main__":
    # Keep this aligned with `websocket/docker-compose.yml`
    print("\n" + "="*60)
    print("WebSocket Server Starting...")
    print("="*60)
    print("Host: 0.0.0.0:8590")
    print("Connect with: ws://localhost:8590/")
    print("CORS enabled for all origins")
    print("⚡ Async mode: gevent")
    print("="*60 + "\n")
    socketio.run(app, host="0.0.0.0", port=8590, debug=False)