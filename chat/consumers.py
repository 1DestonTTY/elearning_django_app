import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #get room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        #add the user to the redis group for this room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        #remove the user from the redis group when they leave
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        #catch the message sent by the user
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        username = text_data_json.get('username', 'Anonymous')

        #broadcast message to the entire redis group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    #this function is triggered by group_send to push the message out to the web page
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))