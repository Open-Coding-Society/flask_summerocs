const socket = io("wss://flask-ws.opencodingsociety.com", { transports: ["websocket"] });

socket.on("player_update", (data) => {
  // Render all players
  for (const [sid, pos] of Object.entries(data.players)) {
    // draw player at pos.x, pos.y
  }
});

function movePlayer(newX, newY) {
  socket.emit("move", { x: newX, y: newY });
}

// Optionally handle player_left to remove avatars
socket.on("player_left", ({sid}) => {
  // remove player from render
});