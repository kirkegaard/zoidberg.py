from cobe.brain import Brain
import re

brain = Brain("tmp/zoidberg.brain")


class Brain():

    def __init__(self, bot):
        self.bot = bot

    def on_message(self, context):
        if context.author == self.bot.ID or context.content.startswith('!'):
            return

        reply = None
        content = re.sub(r'<@.*?>', '', context.content).strip()

        if context.content.startswith('<@%s>' % self.bot.ID):
            while reply == None:
                try:
                    reply = brain.reply(content)
                    context.send(f'<@{context.author}> {reply}')
                except AbortException:
                    return False
                except RetryException:
                    reply = None

        if len(content) >= 4:
            print('Learning from: {}'.format(content))
            brain.learn(content)


def setup(bot):
    return Brain(bot)
