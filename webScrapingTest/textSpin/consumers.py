import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

# class ArticleInputConsumer(WebsocketConsumer):
class ArticleInputConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('test1234', self.channel_name)
        # self.channel_name = "test123"
        await self.accept()
        # print(f"channel_name: {self.channel_name}")
        await self.send(text_data=json.dumps({
            'message': "conexion con ws iniciada"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('test1234',self.channel_name)
        pass

    async def send_message(self, event):
        print(f"send message start -> data {event}")
        payload = event['payload']
        await self.send(text_data=json.dumps(payload))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))