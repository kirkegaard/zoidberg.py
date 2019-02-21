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
