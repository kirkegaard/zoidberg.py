import re
import requests


class Wttr():

    def __init__(self, bot):
        pass

    def weather(self, context, *location: str):
        r = requests.get('https://wttr.in/%s?1nT' % '+'.join(location))
        if r.status_code == 200:
            w = re.sub(r'\s+(New feature.*|Follow.*)\s*$',
                       '', r.text, flags=re.M)
            context.send('```%s```' % w)


def setup(bot):
    return Wttr(bot)
