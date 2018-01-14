import re
import logging
from channels import Group
from channels.sessions import channels_sessions
from .models import Game, GameSquare
from channels.auth import channesl_session_user
from channels.generic.websockets import JsonWebsocketConsumer
log = logging.getLogger(__name__)

class LobbyConsumer(JonWebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        return ['lobby']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept":True})
        pass

    def receive(self, content, **kwargs):
        http_user = True

    def disconnected(self, message, **kwargs):
        pass
