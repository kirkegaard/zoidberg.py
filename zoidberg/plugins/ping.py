import requests


class Ping:
    def __init__(self, bot):
        self.bot = bot

    def on_message(self, context):
        msg = context.Message.content.lower()
        if msg.startswith("ping"):
            context.send("Pong!")


def setup(bot):
    return Ping(bot)
