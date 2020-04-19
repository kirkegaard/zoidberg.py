from slack import WebClient
from slack.errors import SlackApiError
from importlib import import_module, reload
import re
import sys
import time
import logging

from .context import Context

logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class Client:

    SLACKCLIENT = None
    OAUTH_TOKEN = None

    PLUGIN_PATH = "zoidberg.plugins"
    PLUGINS = {}

    TRIGGER = "!"

    def __init__(self, OAUTH_TOKEN):
        logger.info("Starting Zoidberg")
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.SLACKCLIENT = WebClient(token=OAUTH_TOKEN, run_async=True)

    def load_plugins(self, plugins):
        for plugin in plugins:
            self.load_plugin(plugin)

    def load_plugin(self, name):
        if name in self.PLUGINS:
            logger.info("Plugin already loaded [%s]", name)
            return False

        try:
            module = "%s.%s" % (self.PLUGIN_PATH, name)

            if module not in sys.modules:
                plugin = import_module("." + name, package=self.PLUGIN_PATH)
            else:
                plugin = reload(sys.modules[module])

            logger.info("Loading plugin [%s]", name)
            self.PLUGINS[name] = plugin.setup(self)
        except Exception as e:
            raise e

    def reload_plugin(self, name):
        logger.info("Reloading plugin [%s]", name)
        self.unload_plugin(name)
        self.load_plugin(name)

    def unload_plugin(self, name):
        logger.info("Unloading plugin [%s]", name)
        self.PLUGINS.pop(name, None)

    async def handle_event(self, payload):
        event = payload.get("event")

        if hasattr(self, "on_%s" % event["type"]):
            getattr(self, "on_%s" % event["type"])(event)

        context = Context(self, event)

        for name, plugin in self.PLUGINS.items():
            event_type = event["type"].replace("app_", "")
            if hasattr(plugin, "on_%s" % event_type):
                getattr(plugin, "on_%s" % event_type)(context)

            if "text" in event:
                if event["text"].startswith(self.TRIGGER):
                    args = event["text"].split(" ")
                    trigger = args[0][1:]
                    if trigger in dir(plugin):
                        getattr(plugin, trigger)(context, *args[1:])

    def on_hello(self, event):
        self.on_connected(event)

    def on_connected(self, event):
        pass

    def on_message(self, event):
        pass

    def on_mention(self, event):
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
