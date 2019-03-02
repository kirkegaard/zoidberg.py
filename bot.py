import os
from zoidberg.client import Client

if __name__ == "__main__":
    bot = Client(os.environ.get('ZOIDBERG_OAUTH_BOT_TOKEN'))
    bot.load_plugins([
        'wttr',
        'brain',
        'status',
        'dadjoke',
        'utilities'
    ])
    bot.connect()
