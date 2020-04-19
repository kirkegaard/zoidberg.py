from cobe.brain import Brain
import re
import logging

brain = Brain("tmp/zoidberg.brain")
logger = logging.getLogger(__name__)


class Brain:
    def __init__(self, bot):
        self.bot = bot

    def on_mention(self, context):
        content = context.Message.content
        author = context.Author.id

        reply = None
        question = re.sub(r"<@.*?>", "", content).strip()
        while reply == None:
            try:
                reply = brain.reply(question)
                reply = re.sub(r"<@.*?>", "", reply).strip()
                context.send(f"<@{author}> {reply}")
            except AbortException:
                return False
            except RetryException:
                reply = None

    def on_message(self, context):
        content = context.Message.content

        if content.startswith("!"):
            return

        question = re.sub(r"<@.*?>", "", content).strip()
        if len(content) >= 4:
            logger.info("Learning from: %s", question)
            brain.learn(question)


def setup(bot):
    return Brain(bot)
