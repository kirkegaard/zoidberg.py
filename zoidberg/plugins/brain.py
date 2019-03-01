from cobe.brain import Brain
import re
import logging

brain = Brain("tmp/zoidberg.brain")


class Brain():

    def __init__(self, bot):
        self.bot = bot

    def on_message(self, context):
        content = context.Message.content
        author = context.Author.id

        if author == self.bot.ID or content.startswith('!'):
            return

        reply = None
        question = re.sub(r'<@.*?>', '', content).strip()

        if content.startswith('<@%s>' % self.bot.ID):
            while reply == None:
                try:
                    reply = brain.reply(question)
                    context.send(f'<@{author}> {reply}')
                except AbortException:
                    return False
                except RetryException:
                    reply = None

        if len(content) >= 4:
            logging.info('Learning from: %s', question)
            brain.learn(question)


def setup(bot):
    return Brain(bot)
