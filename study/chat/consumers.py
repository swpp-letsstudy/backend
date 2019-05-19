from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
import json

from study.models import StudyGroup, Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user = User.objects.filter(id=data['userId'])[0]
        study_group = StudyGroup.objects.filter(id=data['groupId'])[0]
        print(user, study_group)
        Message.objects.create(user=user, study_group=study_group, content=data['content'])
