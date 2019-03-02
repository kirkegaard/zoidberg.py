from slackclient import SlackClient
from importlib import import_module, reload
import re
import sys
import time
import logging

from .context import Context

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Client():

    SLACKCLIENT = None
    OAUTH_TOKEN = None
    ID = None
    READ_DELAY = 0.5

    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    PLUGIN_PATH = 'zoidberg.plugins'
    PLUGINS = {}

    TRIGGER = '!'

    def __init__(self, OAUTH_TOKEN):
        logging.info('Initializing zoidberg')
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.SLACKCLIENT = SlackClient(OAUTH_TOKEN)

    def load_plugins(self, plugins):
        for plugin in plugins:
            self.load_plugin(plugin)

    def load_plugin(self, name):
        if name in self.PLUGINS:
            logging.info('Plugin already loaded: %s', name)
            return False

        try:
            module = '%s.%s' % (self.PLUGIN_PATH, name)

            if module not in sys.modules:
                plugin = import_module('.' + name, package=self.PLUGIN_PATH)
            else:
                plugin = reload(sys.modules[module])

            logging.info('Loading plugin: %s', name)
            self.PLUGINS[name] = plugin.setup(self)
        except Exception as e:
            raise e

    def reload_plugin(self, name):
        logging.info('Reloading plugin: %s', name)
        self.unload_plugin(name)
        self.load_plugin(name)

    def unload_plugin(self, name):
        logging.info('Unloading plugin: %s', name)
        self.PLUGINS.pop(name, None)

    # We should probably convert this to an async loop if we wanna have
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
            logging.debug('Received event: %s', event)

            if 'subtype' in event:
                break

            if not 'type' in event:
                break

            if hasattr(self, 'on_%s' % event['type']):
                getattr(self, 'on_%s' % event['type'])(event)

            context = Context(self, event)

            for name, plugin in self.PLUGINS.items():
                if hasattr(plugin, 'on_%s' % event['type']):
                    getattr(plugin, 'on_%s' % event['type'])(context)

                if 'text' in event:
                    if event['text'].startswith(self.TRIGGER):
                        args = event['text'].split(' ')
                        trigger = args[0][1:]
                        if trigger in dir(plugin):
                            getattr(plugin, trigger)(context, *args[1:])
                            break

    def on_hello(self, event):
        self.on_connected(event)

    def on_connected(self, event):
        pass

    def on_message(self, event):
        pass

    def on_bot_added(self, event):
        pass

    def on_commands_changed(self, event):
        pass

    def on_apps_changed(self, event):
        pass

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

    # def post_message(self, **kwargs):
    #     self.SLACKCLIENT.rtm_send_message(kwargs)
