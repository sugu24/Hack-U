import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class Consumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        self.accept()

    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def send_message(self, event):
        flag = event['flag']
        post_id = event['post_id']
        number = event['number']
        self.send(text_data=json.dumps({
            'flag' : flag,
            'post_id' : post_id,
            'number' : number
        }))
    

    def delete_message(self, event):
        flag = event['flag']
        response = event['response']
        delete = event['delete']
        self.send(text_data=json.dumps({
            'flag' : flag,
            'response' : response,
            'delete' : delete
        }))
