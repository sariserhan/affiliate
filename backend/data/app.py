import asyncio
import logging

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from typing import List
from database import DETA

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Initialize Deta Base
db = DETA(db="items_db")

# Store the list of connected websockets
connected_websockets: List[WebSocket] = []

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)

    try:
        while True:
            # Create a Deta Stream for database changes
            stream = db.watch()
            print(db)

            async for change in stream:
                # Perform any necessary checks or actions based on database changes
                # ...

                # Broadcast the database change event to connected websockets
                for ws in connected_websockets:
                    await ws.send_text("Database change event detected")

                # Add any additional logic as needed
                # ...

            # Sleep or wait for the next event
            await asyncio.sleep(1)
    finally:
        connected_websockets.remove(websocket)
        
if __name__ == "__main__":
    pass
