class Utilities():

    def __init__(self, bot):
        self.bot = bot

    def load(self, context, plugin):
        self.bot.load_plugin(plugin)

    def reload(self, context, plugin):
        self.bot.reload_plugin(plugin)

    def unload(self, context, plugin):
        self.bot.unload_plugin(plugin)


def setup(bot):
    return Utilities(bot)
