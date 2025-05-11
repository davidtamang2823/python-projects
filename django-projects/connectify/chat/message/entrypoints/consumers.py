import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PrivateMessageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()  # Accept WebSocket connection

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # Parse incoming JSON (e.g., {"message": "hello world"})
            data = json.loads(text_data)
            
            # Extract the "message" field (or use a default)
            received_message = data.get("message", "No message provided")
            
            # Reply with the same structure
            response = {
                "message": received_message,  # Echo back the message
                "type": "response"
            }
            
            await self.send(text_data=json.dumps(response))
            
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))

    async def disconnect(self, close_code):
        pass

class PublicMessageConsumer(AsyncWebsocketConsumer):
    """Not Implemented"""