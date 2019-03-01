class Context():
    """Handles context for en event and returns the proper object"""

    def __init__(self, client, event):
        self.client = client

        if 'user' in event:
            self.Author = Author(event.get('user'))

        if 'text' in event:
            self.Message = Message(event)

        if 'channel' in event:
            self.Channel = Channel(event['channel'])

    # This should be an alias to client send message
    def send(self, message, channel=None):
        if channel is None:
            channel = self.Channel.id

        self.client.SLACKCLIENT.rtm_send_message(
            channel=channel,
            message=message
        )


class Message(Context):

    def __init__(self, event):
        self.content = event.get('text')
        self.timestamp = event.get('ts')


class Author(Context):

    def __init__(self, user):
        # maybe we should fetch the user from the api so we can get a complete
        # user profile
        if type(user) is str:
            self.id = user
            return

        self.id = user.get('id')
        self.team_id = user.get('team_id')

        self.name = user.get('name')
        self.real_name = user.get('real_name')

        profile = user.get('profile', {})

        self.display_name = profile.get('display_name')
        self.firstname = profile.get('first_name')
        self.lastname = profile.get('last_name')

        self.title = profile.get('title')
        self.phone = profile.get('phone')
        self.email = profile.get('email')
        self.skype = profile.get('skype')

        self.status = Status(
            text=profile.get('status_text'),
            emoji=profile.get('status_emoji'),
            expiration=profile.get('status_expiration')
        )

        self.is_bot = user.get('is_bot')
        self.is_admin = user.get('is_admin')
        self.is_owner = user.get('is_owner')
        self.is_primary_owner = user.get('is_primary_owner')


class Status():

    def __init__(self, text, emoji=None, expiration=None):
        self.status_text = text
        self.status_emoji = emoji
        self.status_expiration = expiration


class Channel(Context):

    def __init__(self, id):
        self.id = id
