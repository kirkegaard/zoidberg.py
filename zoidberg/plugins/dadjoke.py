import requests


class Dadjoke:
    def __init__(self, bot):
        self.bot = bot

    def dadjoke(self, context):
        headers = {"Accept": "text/plain"}
        res = requests.get("https://icanhazdadjoke.com", headers=headers)
        context.send(res.text)


def setup(bot):
    return Dadjoke(bot)
