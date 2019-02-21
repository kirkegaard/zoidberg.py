from slackclient import SlackClient
from importlib import import_module
import re
import time

from sanic import Sanic

from .message import Message


class Client():

    SLACKCLIENT = None
    OAUTH_TOKEN = None
    ID = None
    READ_DELAY = 0.5

    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    PLUGIN_PATH = 'zoidberg.plugins'
    PLUGINS = []

    TRIGGER = '!'

    def __init__(self, OAUTH_TOKEN):
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.SLACKCLIENT = SlackClient(OAUTH_TOKEN)
        self.SANIC = Sanic()
        self.SANIC.run(host='127.0.0.1', port=5000)

    def load_plugins(self, plugins):
        for plugin in plugins:
            self.load_plugin(plugin)

    def load_plugin(self, name):
        try:
            plugin = import_module('.' + name, package=self.PLUGIN_PATH)
            self.PLUGINS.append(plugin.setup(self))
        except Exception as e:
            raise e

    # We should probably convert this to an async loop if we want to work with
    # sockets for working with like slash commands
    def connect(self):
        if self.SLACKCLIENT.rtm_connect(with_team_state=False):
            self.ID = self.SLACKCLIENT.api_call("auth.test")["user_id"]
            while True:
                self.handle_events(self.SLACKCLIENT.rtm_read())
                time.sleep(self.READ_DELAY)
        else:
            print('Failed to connect to RTM')

    def handle_events(self, events):
        for event in events:
            if 'subtype' in event:
                break

            if not 'type' in event:
                break

            print(event['type'])

            if event['type'] == 'hello':
                self.on_connected(event)

            if event['type'] == 'message':
                self.on_message(event)
                # if self.is_mention(event):
                #     self.on_mention(event)

            if event['type'] == 'user_typing':
                self.on_user_typing(event)

            if event['type'] == 'user_change':
                self.on_user_change(event)

            if event['type'] == 'channel_joined':
                self.on_channel_joined(event)

            if event['type'] == 'channel_left':
                self.on_channel_left(event)

            if event['type'] == 'channel_created':
                self.on_channel_created(event)

            if event['type'] == 'channel_deleted':
                self.on_channel_deleted(event)

            if event['type'] == 'member_joined_channel':
                self.on_member_joined_channel(event)

            if event['type'] == 'member_left_channel':
                self.on_member_left_channel(event)

            if event['type'] == 'bot_added':
                pass

            if event['type'] == 'commands_changed':
                pass

            if event['type'] == 'apps_changed':
                pass

    def on_connected(self, event):
        pass

    def on_message(self, event):
        for plugin in self.PLUGINS:
            message = Message(event, self)

            if event['text'].startswith(self.TRIGGER):
                args = event['text'].split(' ')
                trigger = args[0][1:]
                if trigger in dir(plugin):
                    getattr(plugin, trigger)(message, *args[1:])
                    break

            if 'on_message' in dir(plugin):
                plugin.on_message(message)

    def on_member_joined_channel(self, event):
        pass

    def on_member_left_channel(self, event):
        pass

    def on_channel_joined(self, event):
        pass

    def on_channel_left(self, event):
        pass

    def on_channel_created(self, event):
        pass

    def on_channel_deleted(self, event):
        pass

    def on_user_typing(self, event):
        pass

    def on_user_change(self, event):
        pass

    def on_mention(self, event):
        pass

    def is_mention(self, event):
        matches = re.search(self.MENTION_REGEX, event['text'])
        if matches:
            return True
        return False

    def post_message(self, channel, response):
        self.SLACKCLIENT.rtm_send_message(
            channel=channel,
            message=response
        )
