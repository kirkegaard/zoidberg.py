from zoidberg.client import Client

if __name__ == "__main__":
    bot = Client(os.environ.get('ZOIDBERG_OAUTH_BOT_TOKEN'))
    bot.load_plugins([
        'brain',
        'dadjoke',
        'vimeo'
    ])
    bot.connect()
