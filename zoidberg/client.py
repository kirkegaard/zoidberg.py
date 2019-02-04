from slackclient import SlackClient
from importlib import import_module
import re
import time


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

    def load_plugins(self, plugins):
        for plugin in plugins:
            self.load_plugin(plugin)

    def load_plugin(self, name):
        try:
            plugin = import_module('.' + name, package=self.PLUGIN_PATH)
            self.PLUGINS.append(plugin.setup(self))
        except Exception as e:
            raise e

    def connect(self):
        if self.SLACKCLIENT.rtm_connect(with_team_state=False):
            self.ID = self.SLACKCLIENT.api_call("auth.test")["user_id"]
            while True:
                self.handle_events(self.SLACKCLIENT.rtm_read())
                time.sleep(self.READ_DELAY)

    def handle_events(self, events):
        for event in events:
            if 'subtype' in event:
                break

            if event['type'] == 'message':
                self.on_message(event)
                # if self.is_mention(event):
                #     self.on_mention(event)

            if event['type'] == 'user_typing':
                self.on_user_typing(event)

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

    def on_channel_joined(self, event):
        pass

    def on_channel_left(self, event):
        pass

    def on_member_joined_channel(self, event):
        pass

    def on_member_left_channel(self, event):
        pass

    def on_channel_created(self, event):
        pass

    def on_channel_deleted(self, event):
        pass

    def on_user_typing(self, event):
        pass

    def on_mention(self, event):
        pass

    def is_mention(self, event):
        matches = re.search(self.MENTION_REGEX, event['text'])
        if matches:
            return True
        return False

    # rewrite this to use rtm
    # https://slackapi.github.io/python-slackclient/real_time_messaging.html#sending-messages-via-the-rtm-api
    def post_message(self, channel, response):
        self.SLACKCLIENT.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )


class Message():

    content = None
    author = None
    channel = None
    client = None

    def __init__(self, event, client):
        self.content = event['text']
        self.author = event['user']
        self.channel = event['channel']
        self.client = client

    def send(self, message):
        self.client.post_message(self.channel, message)
