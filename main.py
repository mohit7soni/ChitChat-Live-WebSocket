from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FastAPI WebSocket Chat</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">

  <style>
    body {
      background: linear-gradient(135deg, #89f7fe, #66a6ff);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-container {
      background: #fff;
      border-radius: 15px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.15);
      width: 100%;
      max-width: 600px;
      padding: 20px;
    }
    .chat-header {
      text-align: center;
      margin-bottom: 15px;
    }
    .chat-header h1 {
      font-size: 1.8rem;
      color: #333;
    }
    #messages {
      list-style-type: none;
      padding: 0;
      max-height: 300px;
      overflow-y: auto;
      margin-bottom: 15px;
    }
    #messages li {
      background: #f1f1f1;
      padding: 10px 15px;
      border-radius: 20px;
      margin-bottom: 8px;
      width: fit-content;
      max-width: 80%;
      word-wrap: break-word;
    }
    #messages li.self {
      background: #007bff;
      color: white;
      margin-left: auto;
    }
    .form-control {
      border-radius: 20px;
    }
    button {
      border-radius: 20px;
      padding: 8px 20px;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <div class="chat-header">
      <h1>FastAPI WebSocket Chat</h1>
      <h6>Your ID: <span id="ws-id" class="text-primary fw-bold"></span></h6>
    </div>

    <ul id="messages"></ul>

    <form id="chatForm" onsubmit="sendMessage(event)" class="d-flex">
      <input type="text" class="form-control me-2" id="messageText" placeholder="Type a message..." autocomplete="off"/>
      <button class="btn btn-primary">Send</button>
    </form>
  </div>

  <script>
    var client_id = Date.now();
    document.querySelector("#ws-id").textContent = client_id;

   var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
var ws = new WebSocket(`${ws_scheme}://${window.location.host}/ws/${client_id}`);

    ws.onmessage = function(event) {
      var messages = document.getElementById('messages');
      var message = document.createElement('li');
      var content = document.createTextNode(event.data);

      if (event.data.startsWith(client_id)) {
        message.classList.add("self");
      }

      message.appendChild(content);
      messages.appendChild(message);
      messages.scrollTop = messages.scrollHeight; // auto-scroll
    };

    function sendMessage(event) {
      var input = document.getElementById("messageText");
      if (input.value.trim() !== "") {
        ws.send(input.value);
        input.value = '';
      }
      event.preventDefault();
    }
  </script>
</body>
</html>

"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    
manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try: 
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")


