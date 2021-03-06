from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework.authtoken.models import Token

from study.study_groups.models import StudyGroup


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.isLoggedIn = False
        self.group_names = set()
        await self.accept()

    async def receive_json(self, content):
        study_group_id = content['groupId']
        token = content['token']
        command = content['command']

        self.validate_user(token)

        # Use StudyGroup.id as a channel_layer group name
        group_name = str(study_group_id)

        if command == 'join':
            await self.join(group_name)
        elif command == 'message':
            await self.message_to_group(group_name, content)

    async def validate_user(self, token):
        if not self.isLoggedIn:
            if Token.objects.filter(key=token).exists():
                self.isLoggedIn = True
            else:
                self.close()

    def group_name(self, study_group_id):
        return str(study_group_id)

    async def join(self, study_group_id):
        group_name = self.group_name(study_group_id)
        if group_name in self.group_names:
            await self.send_error('Already in the group: {}'.format(study_group_id))
        elif StudyGroup.objects.filter(id=study_group_id).exists():
            await self.add_channel_to_group(group_name)
            self.group_names.add(group_name)
        else:
            await self.send_error('The groupId is not valid: {}'.format(study_group_id))

    async def send_error(self, error_msg):
        await self.send_json({'error': error_msg})

    async def disconnect(self, code):
        for group_name in self.group_names:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def add_channel_to_group(self, group_name):
        await self.channel_layer.group_add(group_name, self.channel_name)

    async def message_to_group(self, group_name, content):
        await self.channel_layer.group_send(
            group_name, {
                'type': 'group.message',
                **content,
            })

    # Function name group_message handles payloads with 'group.message' type.
    async def group_message(self, content):
        await self.send_json(content)
