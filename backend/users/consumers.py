# myapp/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .serializers import DeviceDataSerializer

class DeviceDataConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Handle disconnection, you can add cleanup logic here if needed
        pass

    async def receive_json(self, content, **kwargs):
        # Process the data received from the WebSocket
        # This assumes the received content is a dictionary
        # Modify as needed to fit the structure of your incoming WebSocket data
        try:
            data = []
            for ip, values in content.items():
                data.append({
                    'ip_address': ip,
                    'current': values.get('CURRENT'),
                    'power': values.get('POWER'),
                    'voltage': values.get('VOLTAGE'),
                    'user': values.get('user'),
                    'status': values.get('status')
                })

            serializer = DeviceDataSerializer(data=data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {'message': 'Data saved successfully', 'data': serializer.data}
            else:
                response = {'message': 'Invalid data', 'errors': serializer.errors}

        except Exception as e:
            response = {'message': 'Error processing data', 'error': str(e)}

        # Send a JSON response back to the WebSocket client
        await self.send_json(response)
